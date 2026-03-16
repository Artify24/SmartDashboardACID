// Mock API implementation
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export const api = {
  get: async (endpoint) => {
    await delay(600); // Simulate network latency
    console.log(`GET ${endpoint}`);
    return mockDb[endpoint] || null;
  },
  post: async (endpoint, data) => {
    await delay(600);
    console.log(`POST ${endpoint}`, data);
    return { success: true, data };
  }
};

const mockDb = {
  '/dashboard/stats': {
    revenue: 12450000,
    revenueGrowth: 12.5,
    marketShare: 28,
    marketShareGrowth: 2.1,
    competitorActivity: 145,
    competitorActivityGrowth: 15,
    customerSentiment: 78, // NPS
  },
  '/competitors': [
    { id: 1, name: "TechFlow", marketShare: 15, growth: 5.2, revenue: "8.5M", status: "Active", threatLevel: "High" },
    { id: 2, name: "InnovateX", marketShare: 12, growth: -1.5, revenue: "6.2M", status: "Active", threatLevel: "Medium" },
    { id: 3, name: "SoftSystems", marketShare: 8, growth: 2.1, revenue: "4.1M", status: "Watch", threatLevel: "Low" },
    { id: 4, name: "DataCore", marketShare: 22, growth: 8.9, revenue: "15.2M", status: "Active", threatLevel: "High" },
    { id: 5, name: "CloudNine", marketShare: 5, growth: 12.0, revenue: "2.8M", status: "New", threatLevel: "Medium" },
  ],
  '/activity': [
    { id: 1, type: "pricing", company: "TechFlow", title: "Increased Enterprise Plan Pricing", date: "2h ago", description: "TechFlow raised their enterprise tier by 15%." },
    { id: 2, type: "feature", company: "InnovateX", title: "Launched AI Analytics Module", date: "5h ago", description: "New beta feature released for premium users." },
    { id: 3, type: "marketing", company: "DataCore", title: "Super Bowl Ad Campaign", date: "1d ago", description: "Major brand awareness push estimated at $5M." },
    { id: 4, type: "hiring", company: "CloudNine", title: "Hired new VP of Sales", date: "2d ago", description: "Former Salesforce exec joins the team." },
  ]
};
