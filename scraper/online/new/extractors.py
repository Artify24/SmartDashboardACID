import re
import time
from typing import List, Dict, Set, Any, Optional
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import config
from utils import normalize_text, extract_price, filter_duplicates, limit_list, validate_text_length


# ======================================================================
# BASE
# ======================================================================

class BaseExtractor:
    """Base class for all extractors"""

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def safe_extract(self, method, *args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            self.logger.debug(f"Extraction error: {e}")
            return None


# ======================================================================
# META
# ======================================================================

class MetaExtractor(BaseExtractor):
    def get_title(self) -> str:
        try:
            return normalize_text(self.driver.title)
        except:
            return ""

    def get_meta_description(self) -> str:
        try:
            meta = self.driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
            return normalize_text(meta.get_attribute("content"))
        except:
            return ""


# ======================================================================
# HEADINGS
# ======================================================================

class HeadingExtractor(BaseExtractor):
    def extract_headings(self) -> Dict[str, List[str]]:
        headings = {"h1": [], "h2": [], "h3": []}

        try:
            for tag in headings:
                for el in self.driver.find_elements(By.TAG_NAME, tag)[:config.MAX_HEADINGS]:
                    text = normalize_text(el.text)
                    if len(text) > 3:
                        headings[tag].append(text)
        except Exception as e:
            self.logger.debug(f"Heading extraction error: {e}")

        return headings


# ======================================================================
# PRICING + PRICING INTELLIGENCE
# ======================================================================

class PricingExtractor(BaseExtractor):
    """Extract pricing + pricing intelligence"""

    PRICE_SIGNAL_REGEX = re.compile(r"(₹|Rs\.?|INR|\$|€)\s*[\d,]+", re.I)
    BILLING_UNIT_REGEX = re.compile(r"(per|/)\s*(month|year|mo|yr|user|seat|agent)", re.I)
    GATING_REGEX = re.compile(r"(contact|custom|request\s+demo|talk\s+to\s+sales)", re.I)

    def extract_pricing(self) -> Dict[str, Any]:
        plans = []
        cards = []

        # Allow JS pricing to render
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.find_elements(
                    By.XPATH,
                    "//*[contains(text(),'₹') or contains(text(),'INR') or contains(text(),'Free')]"
                )
            )
        except:
            pass

        # Primary selectors
        for selector in config.PRICING_SELECTORS:
            try:
                cards.extend(self.driver.find_elements(By.XPATH, selector))
            except:
                pass

        # Aggressive fallbacks
        if not cards:
            for sel in [
                "[class*='pricing']", "[class*='price']", "[class*='plan']",
                "[class*='tier']", "[data-testid*='price']", "[data-testid*='plan']"
            ]:
                try:
                    cards.extend(self.driver.find_elements(By.CSS_SELECTOR, sel))
                except:
                    pass

        # Table fallback
        try:
            for table in self.driver.find_elements(By.TAG_NAME, "table"):
                if re.search(r"(₹|INR|free|contact)", table.text, re.I):
                    cards.append(table)
        except:
            pass

        seen = set()

        for card in cards[: config.MAX_PRICING_CARDS * 3]:
            try:
                plan = self._extract_plan_data(card, seen)
                if plan:
                    plans.append(plan)
            except Exception as e:
                self.logger.debug(f"Pricing card error: {e}")

        return {
            "plans": plans,
            "pricing_model": self._infer_pricing_model(),
            "price_evidence": self._extract_price_evidence(),
            "billing_units": self._extract_billing_units(),
            "gating_signals": self._extract_gating_signals(),
            "confidence": self._confidence_score(plans)
        }

    # ------------------------------------------------------------------

    def _extract_plan_data(self, card, seen: Set) -> Optional[Dict]:
        text = normalize_text(card.text.replace("\xa0", " "))
        if len(text) < 15:
            return None

        plan = self._extract_plan_name(card, text)
        price = self._extract_price(text)
        features = self._extract_features(card, text)

        key = f"{plan}_{price}".lower()
        if key in seen:
            return None

        seen.add(key)

        return {
            "plan": plan,
            "price": price or "Contact Sales",
            "features": features[:15],
            "description": text[:300]
        }

    def _extract_plan_name(self, card, text: str) -> str:
        for tag in ["h1", "h2", "h3", "h4"]:
            for el in card.find_elements(By.TAG_NAME, tag):
                t = normalize_text(el.text)
                if 3 < len(t) < 40 and not re.search(r"(₹|INR|\d|month|year)", t, re.I):
                    return t

        for keyword in ["Free", "Basic", "Starter", "Standard", "Pro", "Premium", "Enterprise"]:
            if keyword.lower() in text.lower():
                return keyword

        return "Plan"

    def _extract_price(self, text: str) -> Optional[str]:
        patterns = [
            r"(?:₹|Rs\.?|INR)\s?[\d,]+(?:\.\d+)?\s*(?:/|per\s*)?(?:month|year|mo|yr)?",
            r"from\s+(?:₹|Rs\.?|INR)\s?[\d,]+",
            r"starting\s+at\s+(?:₹|Rs\.?|INR)\s?[\d,]+",
        ]

        for pat in patterns:
            match = re.search(pat, text, re.I)
            if match:
                return normalize_text(match.group(0))

        if re.search(r"\bfree\b", text, re.I):
            return "Free"

        if re.search(r"contact|custom|talk\s+to\s+sales", text, re.I):
            return "Contact Sales"

        return None

    def _extract_features(self, card, text: str) -> List[str]:
        features = []

        for el in card.find_elements(By.TAG_NAME, "li"):
            t = normalize_text(el.text)
            if validate_text_length(t, 6, 120) and not self._looks_like_price(t):
                features.append(t)

        if not features:
            for line in text.splitlines():
                line = normalize_text(line)
                if validate_text_length(line, 6, 120) and not self._looks_like_price(line):
                    features.append(line)

        return filter_duplicates(features)

    def _looks_like_price(self, text: str) -> bool:
        return bool(re.search(r"(₹|INR|Rs\.?|\d+\s*/\s*(mo|yr)|per\s+(month|year))", text, re.I))

    # ---------------- PRICING INTELLIGENCE ----------------

    def _extract_price_evidence(self) -> List[str]:
        text = normalize_text(self.driver.find_element(By.TAG_NAME, "body").text)
        evidence = []

        for match in self.PRICE_SIGNAL_REGEX.finditer(text):
            snippet = text[max(0, match.start()-40): match.end()+40]
            evidence.append(normalize_text(snippet))

        if "free" in text.lower():
            evidence.append("Free tier mentioned")

        return filter_duplicates(evidence)[:20]

    def _extract_billing_units(self) -> List[str]:
        text = normalize_text(self.driver.find_element(By.TAG_NAME, "body").text)
        return filter_duplicates([m.group(0).lower() for m in self.BILLING_UNIT_REGEX.finditer(text)])

    def _extract_gating_signals(self) -> List[str]:
        text = normalize_text(self.driver.find_element(By.TAG_NAME, "body").text)
        return ["Sales-gated pricing"] if self.GATING_REGEX.search(text) else []

    def _infer_pricing_model(self) -> str:
        text = normalize_text(self.driver.find_element(By.TAG_NAME, "body").text).lower()
        if "free" in text and self.PRICE_SIGNAL_REGEX.search(text):
            return "freemium"
        if self.GATING_REGEX.search(text):
            return "sales-led"
        if self.PRICE_SIGNAL_REGEX.search(text):
            return "transparent"
        return "unknown"

    def _confidence_score(self, plans: List[Dict]) -> float:
        if plans:
            return 0.9
        if self._extract_price_evidence():
            return 0.6
        return 0.3


# ======================================================================
# FEATURES
# ======================================================================

class FeaturesExtractor(BaseExtractor):
    def extract_features(self) -> List[str]:
        features = []
        try:
            for selector in config.FEATURES_SELECTORS:
                for el in self.driver.find_elements(By.XPATH, selector)[:30]:
                    t = normalize_text(el.text)
                    if validate_text_length(t, config.FEATURE_MIN_LENGTH, config.FEATURE_MAX_LENGTH):
                        features.append(t)
        except Exception as e:
            self.logger.debug(f"Features extraction error: {e}")

        return filter_duplicates(features)[:config.MAX_FEATURES]


# ======================================================================
# CTA
# ======================================================================

class CTAExtractor(BaseExtractor):
    def extract_ctas(self) -> List[str]:
        ctas = []

        try:
            for el in self.driver.find_elements(By.TAG_NAME, "button")[:30]:
                text = normalize_text(el.text).lower()
                if any(k in text for k in config.CTA_KEYWORDS):
                    ctas.append(normalize_text(el.text))

            for el in self.driver.find_elements(By.TAG_NAME, "a")[:50]:
                text = normalize_text(el.text).lower()
                if any(k in text for k in config.CTA_KEYWORDS):
                    ctas.append(normalize_text(el.text))
        except Exception as e:
            self.logger.debug(f"CTA extraction error: {e}")

        return limit_list(filter_duplicates(ctas), config.MAX_CTA_BUTTONS)


# ======================================================================
# SOCIAL
# ======================================================================

class SocialExtractor(BaseExtractor):
    def extract_socials(self) -> Dict[str, str]:
        socials = {
            "twitter": None, "linkedin": None, "facebook": None,
            "instagram": None, "github": None, "youtube": None
        }

        try:
            for link in self.driver.find_elements(By.TAG_NAME, "a"):
                href = link.get_attribute("href") or ""
                for platform in socials:
                    if platform in href.lower() and not socials[platform]:
                        socials[platform] = href
        except Exception as e:
            self.logger.debug(f"Social extraction error: {e}")

        return {k: v for k, v in socials.items() if v}


# ======================================================================
# INTEGRATIONS
# ======================================================================

class IntegrationExtractor(BaseExtractor):
    def extract_integrations(self) -> List[str]:
        integrations = []

        try:
            for selector in config.INTEGRATIONS_SELECTORS:
                for el in self.driver.find_elements(By.XPATH, selector)[:30]:
                    text = el.get_attribute("alt") or el.get_attribute("title") or normalize_text(el.text)
                    if text:
                        integrations.append(text)
        except Exception as e:
            self.logger.debug(f"Integration extraction error: {e}")

        return limit_list(filter_duplicates(integrations), config.MAX_INTEGRATIONS)


# ======================================================================
# TRUST
# ======================================================================

class TrustExtractor(BaseExtractor):
    def extract_trust_signals(self) -> Dict[str, List[str]]:
        trust = {"testimonials": [], "certifications": [], "stats": []}

        try:
            for el in self.driver.find_elements(By.XPATH, "//div[contains(@class,'testimonial')]"):
                t = normalize_text(el.text)
                if 20 < len(t) < 500:
                    trust["testimonials"].append(t)

            for el in self.driver.find_elements(By.TAG_NAME, "img"):
                alt = (el.get_attribute("alt") or "").lower()
                if any(k in alt for k in config.CERT_KEYWORDS):
                    trust["certifications"].append(el.get_attribute("alt"))

            for el in self.driver.find_elements(By.XPATH, "//*[contains(text(),'%')]"):
                t = normalize_text(el.text)
                if 5 < len(t) < 100:
                    trust["stats"].append(t)
        except Exception as e:
            self.logger.debug(f"Trust extraction error: {e}")

        return {k: limit_list(filter_duplicates(v), 10) for k, v in trust.items()}
