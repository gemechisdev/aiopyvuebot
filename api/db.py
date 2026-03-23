import os
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

# Setup logging
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    logger.warning(
        "Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY environment variables.")
    supabase = None
else:
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        logger.info("Supabase client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        supabase = None

# SQL for creating the tables in Supabase
"""
-- Run this in the Supabase SQL editor to create your tables

-- Users table
CREATE TABLE public.users (
  id BIGINT PRIMARY KEY,
  target_user JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Whispers table  
CREATE TABLE public.whispers (
  inline_message_id VARCHAR PRIMARY KEY,
  message TEXT NOT NULL,
  sender_id BIGINT REFERENCES public.users(id),
  recipient_ids BIGINT[] NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '7 days')
);

-- Create indexes for better performance
CREATE INDEX idx_users_target ON public.users USING GIN (target_user);
CREATE INDEX idx_whispers_sender ON public.whispers (sender_id);
CREATE INDEX idx_whispers_recipients ON public.whispers USING GIN (recipient_ids);
CREATE INDEX idx_whispers_expires ON public.whispers (expires_at);

-- Set up Row Level Security
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.whispers ENABLE ROW LEVEL SECURITY;

-- Create policies for service role access
CREATE POLICY "Service role can do everything on users" 
ON public.users FOR ALL 
TO service_role 
USING (true) 
WITH CHECK (true);

CREATE POLICY "Service role can do everything on whispers" 
ON public.whispers FOR ALL 
TO service_role 
USING (true) 
WITH CHECK (true);

-- Function to cleanup expired whispers
CREATE OR REPLACE FUNCTION cleanup_expired_whispers()
RETURNS void AS $$
BEGIN
    DELETE FROM public.whispers WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;

-- Updated at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to users table
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON public.users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
"""