'use client';

import React, { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { MapPin, Globe, ArrowRight, ArrowLeft, User, Building2, MapPinned, Sparkles, Check } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { set } from 'react-hook-form';

export default function CompetitionSetupPage() {
    const router = useRouter();
    const [currentStep, setCurrentStep] = useState(0); // 0: mode selection, 1-4: form steps
    const [mode, setMode] = useState(null); // 'local' | 'online'

    const [formData, setFormData] = useState({
        fullName: '',
        businessName: '',
        area: '',
        city: '',
        industry: '',
        businessWebsite: '',
        competitorWebsites: ['']
    });
    console.log('formData:', formData);

    const [isSubmitting, setIsSubmitting] = useState(false);
    const [errors, setErrors] = useState({});
    const [locationChecking, setLocationChecking] = useState({ area: false, city: false });
    const debounceRefs = useRef({});

    const handleModeSelect = (selectedMode) => {
        setMode(selectedMode);
        setCurrentStep(1);
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        validateField(name, value);
        // For location fields, debounce a server-side/name lookup validation
        if (name === 'area' || name === 'city') {
            if (debounceRefs.current[name]) clearTimeout(debounceRefs.current[name]);
            debounceRefs.current[name] = setTimeout(() => validateLocation(name, value), 700);
        }
    };

    const handleCompetitorChange = (index, value) => {
        setFormData(prev => {
            const next = Array.isArray(prev.competitorWebsites) ? [...prev.competitorWebsites] : [];
            next[index] = value;
            return { ...prev, competitorWebsites: next };
        });
        validateCompetitorAt(index, value);
    };

    const addCompetitor = () => {
        setFormData(prev => ({ ...prev, competitorWebsites: [...(prev.competitorWebsites || []), ''] }));
    };

    const removeCompetitor = (index) => {
        setFormData(prev => {
            const next = (prev.competitorWebsites || []).filter((_, i) => i !== index);
            return { ...prev, competitorWebsites: next.length ? next : [''] };
        });
    };

    const handleNext = () => {
        if (currentStep < questions.length) {
            setCurrentStep(currentStep + 1);
        } else {
            handleSubmit();
        }
    };

    const handleBack = () => {
        if (currentStep > 1) {
            setCurrentStep(currentStep - 1);
        } else {
            setCurrentStep(0);
            setMode(null);
        }
    };

    const getQuestions = () => {
        const defaultQuestions = [
            {
                id: 1,
                icon: User,
                title: "Let's start with you!",
                subtitle: mode === 'local' ? "Who's the brilliant mind behind this local venture?" : "Who's leading this digital journey?",
                field: 'fullName',
                placeholder: 'e.g., Sarah Johnson',
                label: 'Your Full Name'
            },
            {
                id: 2,
                icon: Building2,
                title: "What's your business called?",
                subtitle: mode === 'local' ? "Every great local business has a memorable name" : "What's the name that'll dominate the digital space?",
                field: 'businessName',
                placeholder: mode === 'local' ? 'e.g., Sarah\'s Coffee House' : 'e.g., TechFlow Solutions',
                label: 'Business Name'
            },
            {
                id: 3,
                icon: MapPinned,
                title: "Where's your business area?",
                subtitle: mode === 'local' ? "Which neighborhood do you call home?" : "What's your primary market area?",
                field: 'area',
                placeholder: mode === 'local' ? 'e.g., Downtown District' : 'e.g., North America',
                label: 'Business Area'
            },
            {
                id: 4,
                icon: MapPin,
                title: "Which city are you in?",
                subtitle: mode === 'local' ? "Let's pinpoint your exact location" : "What's your headquarters city?",
                field: 'city',
                placeholder: mode === 'local' ? 'e.g., San Francisco' : 'e.g., New York',
                label: 'City'
            }
        ];

        if (mode === 'online') {
            // Replace questions with the user's requested fields for online competitions
            const onlineQuestions = [
                {
                    id: 1,
                    icon: Globe,
                    title: "Industry",
                    subtitle: "Enter your primary industry",
                    field: 'industry',
                    placeholder: 'e.g., Software, Retail, Finance',
                    label: 'Industry'
                },
                {
                    id: 2,
                    icon: Building2,
                    title: "Your Business Name",
                    subtitle: "Provide the exact name of your business",
                    field: 'businessName',
                    placeholder: 'e.g., TechFlow Solutions',
                    label: 'Your Business Name'
                },
                {
                    id: 3,
                    icon: Globe,
                    title: "Your Business Website URL",
                    subtitle: "Provide the full URL for your business website",
                    field: 'businessWebsite',
                    placeholder: 'https://yourbusiness.com',
                    label: 'Your Business Website URL'
                },
                {
                    id: 4,
                    icon: Globe,
                    title: "Competitor Website URL(s)",
                    subtitle: "Provide one or more competitor URLs, comma-separated",
                    field: 'competitorWebsites',
                    placeholder: 'https://competitor1.com, https://competitor2.com',
                    label: 'Competitor Website URL(s)'
                }
            ];

            return onlineQuestions;
        }

        return defaultQuestions;
    };

    const questions = getQuestions();
    const currentQuestion = questions[currentStep - 1];

    const isCurrentStepValid = () => {
        if (!currentQuestion) return false;
        const field = currentQuestion.field;
        if (field === 'competitorWebsites') {
            const arr = formData.competitorWebsites;
            const hasAny = Array.isArray(arr) && arr.some(s => (s || '').trim() !== '');
            const compErrs = errors.competitorWebsites || [];
            const anyErr = Array.isArray(compErrs) && compErrs.some(e => e && e.length > 0);
            return hasAny && !anyErr;
        }
        return (formData[field] || '').toString().trim() !== '' && !(errors[field] && errors[field].length > 0);
    };

    // Validation helpers
    const isDomainOrUrl = (s) => {
        if (!s) return false;
        const val = s.trim();
        // quick domain regex (example.com) or allow full URL with protocol
        const domainRegex = /^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$/i;
        try {
            // If it's a full URL this will succeed
            // eslint-disable-next-line no-new
            new URL(val);
            return true;
        } catch (e) {
            // try adding protocol and test domain regex
            const stripped = val.replace(/^https?:\/\//i, '').replace(/\/$/, '');
            return domainRegex.test(stripped);
        }
    };

    const setFieldError = (field, msg) => {
        setErrors(prev => ({ ...prev, [field]: msg }));
    };

    const validateField = (field, value) => {
        const v = (value || '').toString().trim();
        switch (field) {
            case 'fullName':
                if (!v || v.split(/\s+/).length < 2) setFieldError(field, 'Enter first and last name');
                else setFieldError(field, '');
                break;
            case 'businessName':
                if (!v) setFieldError(field, 'Enter your business name');
                else setFieldError(field, '');
                break;
            case 'industry':
                if (!v) setFieldError(field, 'Enter industry');
                else setFieldError(field, '');
                break;
            case 'businessWebsite':
                if (!v || !isDomainOrUrl(v)) setFieldError(field, 'Enter a valid website or domain (example.com)');
                else setFieldError(field, '');
                break;
            case 'area':
            case 'city':
                if (!v || !/^[a-zA-Z\s\-]{2,}$/.test(v)) setFieldError(field, 'Enter a valid location (letters and spaces only)');
                else setFieldError(field, '');
                break;
            default:
                setFieldError(field, '');
        }
    };

    const validateCompetitorAt = (index, value) => {
        setErrors(prev => {
            const arr = Array.isArray(prev.competitorWebsites) ? [...prev.competitorWebsites] : [];
            arr[index] = (value || '').toString().trim() === '' ? 'Please enter a URL or remove this field' : (isDomainOrUrl(value) ? '' : 'Enter a valid URL/domain');
            return { ...prev, competitorWebsites: arr };
        });
    };

    // Validate location using OpenStreetMap Nominatim (no API key). Debounced caller should be used.
    const validateLocation = async (field, value) => {
        const v = (value || '').toString().trim();
        if (!v || v.length < 2) {
            setFieldError(field, 'Enter a valid location');
            return false;
        }

        setLocationChecking(prev => ({ ...prev, [field]: true }));
        try {
            const q = encodeURIComponent(v);
            const url = `https://nominatim.openstreetmap.org/search?format=json&q=${q}&limit=1`;
            const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
            if (!res.ok) throw new Error('Location lookup failed');
            const data = await res.json();
            if (Array.isArray(data) && data.length > 0) {
                setFieldError(field, '');
                return true;
            } else {
                setFieldError(field, 'Location not found');
                return false;
            }
        } catch (e) {
            setFieldError(field, 'Could not verify location');
            return false;
        } finally {
            setLocationChecking(prev => ({ ...prev, [field]: false }));
        }
    };

    const handleSubmit = async () => {
        setIsSubmitting(true);

        try {
            // Save to localStorage
            const dataToSave = {
                mode,
                ...formData,
                timestamp: new Date().toISOString()
            };
            localStorage.setItem(
                'competition_mode_data',
                JSON.stringify(dataToSave)
            );

            // 1. Scrape OUR site first
            const mainResponse = await fetch('http://127.0.0.1:8000/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url_or_name: formData.businessName,
                    is_our_site: true,
                    max_pages: 10,
                    headless: true,
                    include_social: true
                })
            });

            if (!mainResponse.ok) {
                throw new Error('Failed to scrape primary business');
            }

            // 2. Scrape competitors in parallel
            const competitorRequests = formData.competitorWebsites.map((compUrl) =>
                fetch('http://127.0.0.1:8000/scrape', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        url_or_name: compUrl,
                        is_our_site: false,
                        max_pages: 10,
                        headless: true,
                        include_social: true
                    })
                })
            );

            await Promise.all(competitorRequests);

            // 3. Navigate after all scraping is triggered
            router.push('/dashboard');

        } catch (error) {
            console.error('Submission error:', error);
        } finally {
            setIsSubmitting(false);
        }
    };


    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && isCurrentStepValid()) {
            handleNext();
        }
    };


    const progress = currentStep > 0 && questions.length > 0 ? (currentStep / questions.length) * 100 : 0;

    if (isSubmitting) {
        return (
            <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4 relative overflow-hidden">
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/10 rounded-full blur-3xl animate-pulse" />
                </div>

                <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="flex flex-col items-center space-y-8 relative z-10 text-center"
                >
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{
                            type: "spring",
                            stiffness: 200,
                            damping: 20,
                            delay: 0.2
                        }}
                        className="w-24 h-24 bg-primary text-primary-foreground rounded-full flex items-center justify-center shadow-2xl"
                    >
                        <Check className="w-12 h-12" strokeWidth={3} />
                    </motion.div>

                    <div className="space-y-4">
                        <motion.h2
                            initial={{ y: 20, opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            transition={{ delay: 0.4 }}
                            className="text-4xl font-bold tracking-tight"
                        >
                            All Set, {(formData.fullName || '').split(' ')[0] || 'there'}!
                        </motion.h2>
                        <motion.p
                            initial={{ y: 20, opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            transition={{ delay: 0.6 }}
                            className="text-xl text-muted-foreground"
                        >
                            Preparing your competitive analysis dashboard...
                        </motion.p>
                    </div>

                    <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: 200 }}
                        transition={{ delay: 0.8, duration: 1.5, ease: "easeInOut" }}
                        className="h-1 bg-primary rounded-full"
                    />
                </motion.div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4 relative overflow-hidden">
            {/* Animated background elements */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl opacity-20" />
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/5 rounded-full blur-3xl opacity-20" />
            </div>

            <div className="w-full max-w-3xl space-y-8 relative z-10">
                {/* Progress Bar */}
                {currentStep > 0 && (
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-2"
                    >
                        <div className="flex justify-between text-sm text-muted-foreground">
                            <span>Question {currentStep} of {questions.length}</span>
                            <span>{Math.round(progress)}% Complete</span>
                        </div>
                        <div className="h-2 bg-muted rounded-full overflow-hidden">
                            <motion.div
                                className="h-full bg-gradient-to-r from-primary to-accent"
                                initial={{ width: 0 }}
                                animate={{ width: `${progress}%` }}
                                transition={{ duration: 0.5, ease: "easeOut" }}
                            />
                        </div>
                    </motion.div>
                )}

                <AnimatePresence mode="wait">
                    {currentStep === 0 ? (
                        <motion.div
                            key="mode-selection"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="space-y-8"
                        >
                            {/* Header */}
                            <div className="text-center space-y-3">
                                <motion.div
                                    initial={{ opacity: 0, y: -20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.1 }}
                                >
                                    <h1 className="text-4xl font-bold tracking-tight text-foreground">
                                        Choose Your Arena
                                    </h1>
                                </motion.div>
                                <motion.p
                                    initial={{ opacity: 0, y: -20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.2 }}
                                    className="text-muted-foreground text-lg"
                                >
                                    Where does your competition live?
                                </motion.p>
                            </div>

                            {/* Mode Cards */}
                            <div className="grid md:grid-cols-2 gap-6">
                                <motion.div
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.3 }}
                                >
                                    <Card
                                        className="group relative overflow-hidden cursor-pointer bg-card border-border hover:border-primary transition-all hover:shadow-2xl hover:shadow-primary/10 h-full"
                                        onClick={() => handleModeSelect('local')}
                                    >
                                        <CardContent className="p-8 space-y-6 flex flex-col items-center text-center h-full justify-center">
                                            <div className="relative">
                                                <div className="absolute inset-0 bg-primary/20 rounded-full blur-xl group-hover:blur-2xl transition-all" />
                                                <div className="relative p-6 rounded-full bg-gradient-to-br from-primary/20 to-primary/5 group-hover:scale-110 transition-transform duration-500">
                                                    <MapPin className="w-12 h-12 text-primary" />
                                                </div>
                                            </div>
                                            <div className="space-y-3">
                                                <h3 className="text-3xl font-bold">Local Competition</h3>
                                                <p className="text-muted-foreground text-base">
                                                    Compete with businesses in your neighborhood and city
                                                </p>
                                            </div>
                                            <div className="absolute inset-x-0 bottom-0 h-1.5 bg-gradient-to-r from-transparent via-primary to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                                        </CardContent>
                                    </Card>
                                </motion.div>

                                <motion.div
                                    initial={{ opacity: 0, x: 20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.4 }}
                                >
                                    <Card
                                        className="group relative overflow-hidden cursor-pointer bg-card border-border hover:border-accent transition-all hover:shadow-2xl hover:shadow-accent/10 h-full"
                                        onClick={() => handleModeSelect('online')}
                                    >
                                        <CardContent className="p-8 space-y-6 flex flex-col items-center text-center h-full justify-center">
                                            <div className="relative">
                                                <div className="absolute inset-0 bg-accent/20 rounded-full blur-xl group-hover:blur-2xl transition-all" />
                                                <div className="relative p-6 rounded-full bg-gradient-to-br from-accent/20 to-accent/5 group-hover:scale-110 transition-transform duration-500">
                                                    <Globe className="w-12 h-12 text-accent" />
                                                </div>
                                            </div>
                                            <div className="space-y-3">
                                                <h3 className="text-3xl font-bold">Online Competition</h3>
                                                <p className="text-muted-foreground text-base">
                                                    Analyze digital competitors across the globe
                                                </p>
                                            </div>
                                            <div className="absolute inset-x-0 bottom-0 h-1.5 bg-gradient-to-r from-transparent via-accent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                                        </CardContent>
                                    </Card>
                                </motion.div>
                            </div>
                        </motion.div>
                    ) : (
                        <motion.div
                            key={`question-${currentStep}`}
                            initial={{ opacity: 0, x: 50 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -50 }}
                            transition={{ type: "spring", stiffness: 100, damping: 20 }}
                            className="w-full max-w-2xl mx-auto"
                        >
                            <Card className="border-2 border-primary/10 shadow-2xl overflow-hidden">
                                <CardContent className="p-10 space-y-8">
                                    {/* Question Header */}
                                    <div className="space-y-6">
                                        <div className="flex items-center gap-4">
                                            <motion.div
                                                initial={{ scale: 0, rotate: -180 }}
                                                animate={{ scale: 1, rotate: 0 }}
                                                transition={{ type: "spring", stiffness: 200, damping: 15 }}
                                                className="p-4 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/20"
                                            >
                                                {React.createElement(currentQuestion.icon, { className: "w-8 h-8 text-primary" })}
                                            </motion.div>
                                            <div className="flex-1">
                                                <div className="flex items-center gap-2 mb-1">
                                                    <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                                                        {mode === 'local' ? 'Local Competition' : 'Online Competition'}
                                                    </span>
                                                    <div className="flex items-center gap-1">
                                                        {Array.from({ length: questions.length }, (_, i) => i + 1).map((step) => (
                                                            <div
                                                                key={step}
                                                                className={`w-2 h-2 rounded-full transition-all ${step < currentStep ? 'bg-primary' :
                                                                    step === currentStep ? 'bg-primary w-6' :
                                                                        'bg-muted'
                                                                    }`}
                                                            />
                                                        ))}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        <motion.div
                                            initial={{ opacity: 0, y: 20 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ delay: 0.1 }}
                                            className="space-y-2"
                                        >
                                            <h2 className="text-3xl font-bold tracking-tight">
                                                {currentQuestion.title}
                                            </h2>
                                            <p className="text-lg text-muted-foreground">
                                                {currentQuestion.subtitle}
                                            </p>
                                        </motion.div>
                                    </div>

                                    {/* Input Field */}
                                    <motion.div
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.2 }}
                                        className="space-y-3"
                                    >
                                        <Label htmlFor={currentQuestion.field} className="text-base font-medium">
                                            {currentQuestion.label}
                                        </Label>
                                        {currentQuestion.field === 'competitorWebsites' ? (
                                            <div className="space-y-3">
                                                {(formData.competitorWebsites || []).map((url, idx) => (
                                                    <div key={idx} className="flex items-center gap-2">
                                                        <Input
                                                            id={`competitor-${idx}`}
                                                            name={`competitor-${idx}`}
                                                            placeholder={currentQuestion.placeholder}
                                                            value={url}
                                                            onChange={(e) => handleCompetitorChange(idx, e.target.value)}
                                                            onKeyDown={(e) => { if (e.key === 'Enter' && isCurrentStepValid()) handleNext(); }}
                                                            className="h-14 text-lg px-4 border-2 focus:border-primary transition-all flex-1"
                                                            autoFocus={idx === (formData.competitorWebsites.length - 1)}
                                                        />
                                                        {(formData.competitorWebsites || []).length > 1 && (
                                                            <button type="button" onClick={() => removeCompetitor(idx)} className="inline-flex items-center justify-center h-10 w-10 rounded-md bg-muted text-foreground">
                                                                —
                                                            </button>
                                                        )}
                                                    </div>
                                                ))}

                                                <div>
                                                    <button type="button" onClick={addCompetitor} className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-transparent border border-primary text-primary">
                                                        + Add another competitor
                                                    </button>
                                                </div>
                                                {/* show per-item error if present */}
                                                {errors.competitorWebsites && Array.isArray(errors.competitorWebsites) && (
                                                    <div className="space-y-1">
                                                        {errors.competitorWebsites.map((err, i) => err ? (
                                                            <p key={i} className="text-sm text-destructive">{err}</p>
                                                        ) : null)}
                                                    </div>
                                                )}
                                            </div>
                                        ) : (
                                            <>
                                                <Input
                                                    id={currentQuestion.field}
                                                    name={currentQuestion.field}
                                                    placeholder={currentQuestion.placeholder}
                                                    value={formData[currentQuestion.field] || ''}
                                                    onChange={handleInputChange}
                                                    onKeyPress={handleKeyPress}
                                                    className="h-14 text-lg px-4 border-2 focus:border-primary transition-all"
                                                    autoFocus
                                                />
                                                {(currentQuestion.field === 'area' || currentQuestion.field === 'city') && locationChecking[currentQuestion.field] && (
                                                    <p className="text-sm text-muted-foreground">Verifying location…</p>
                                                )}
                                                {errors[currentQuestion.field] && (
                                                    <p className="text-sm text-destructive">{errors[currentQuestion.field]}</p>
                                                )}
                                            </>
                                        )}
                                        <p className="text-sm text-muted-foreground flex items-center gap-2">
                                            <Sparkles className="w-4 h-4" />
                                            Press Enter to continue
                                        </p>
                                    </motion.div>

                                    {/* Navigation Buttons */}
                                    <div className="flex gap-3 pt-4">
                                        <Button
                                            variant="outline"
                                            onClick={handleBack}
                                            className="flex items-center gap-2"
                                        >
                                            <ArrowLeft className="w-4 h-4" />
                                            Back
                                        </Button>
                                        <Button
                                            onClick={handleNext}
                                            disabled={!isCurrentStepValid()}
                                            className="flex-1 h-12 text-base font-medium"
                                        >
                                            {currentStep === questions.length ? (
                                                <>
                                                    Complete Setup <Check className="ml-2 w-5 h-5" />
                                                </>
                                            ) : (
                                                <>
                                                    Continue <ArrowRight className="ml-2 w-5 h-5" />
                                                </>
                                            )}
                                        </Button>
                                    </div>
                                </CardContent>
                            </Card>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
