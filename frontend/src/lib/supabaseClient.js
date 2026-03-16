import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  // Warn during development if env vars are missing
  // In production ensure these are set in your deployment platform.
  // Do NOT commit private/service keys to source control.
  // eslint-disable-next-line no-console
  console.warn('Missing NEXT_PUBLIC_SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY in environment. Supabase client may fail to initialize.');
}

export const supabase = createClient(supabaseUrl || '', supabaseAnonKey || '');

export async function getCompetitiveIntel() {
  try {
    const { data, error } = await supabase
      .from('llm_outputs')
      .select('id, type, content, created_at')
      .in('type', ['competitorSummary'])
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Supabase error:', error);
      return [];
    }

    return data || [];
  } catch (e) {
    console.error('Unexpected error fetching competitive intel:', e);
    return [];
  }
}