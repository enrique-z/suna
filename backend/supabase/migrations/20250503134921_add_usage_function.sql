-- Migration to add a function for calculating total LLM usage and cost.

CREATE OR REPLACE FUNCTION get_llm_usage(account_id uuid)
RETURNS TABLE (
    model text,
    tokens_used bigint,
    cost numeric
) SECURITY DEFINER
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        m.model,
        COALESCE(SUM(m.prompt_tokens + m.completion_tokens)::bigint, 0) as tokens_used,
        COALESCE(SUM(m.cost), 0) as cost
    FROM llm_usage m
    WHERE m.account_id = get_llm_usage.account_id
    GROUP BY m.model;
END;
$$;

-- Grant execute permission to relevant roles
GRANT EXECUTE ON FUNCTION public.get_llm_usage TO authenticated, service_role;

-- Optional: Revoke default public execute if needed for stricter security
-- REVOKE EXECUTE ON FUNCTION public.get_total_project_usage() FROM PUBLIC;