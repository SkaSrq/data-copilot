examples = [
    {
        "query": """WITH DailySales AS (
    SELECT 
        DATE(date_created) AS sale_date,
        SUM(CASE WHEN name LIKE '%CAPS%' THEN acq_gross_revenue + rep_gross_revenue ELSE 0 END) AS capsule_sales,
        SUM(acq_gross_revenue + rep_gross_revenue) AS total_sales
    FROM products
    GROUP BY DATE(date_created)
)

SELECT 
    AVG((capsule_sales / total_sales) * 100) AS avg_daily_capsule_sales_percentage
FROM DailySales;
""",
        "explanation": "Which % of average daily sales comes from Capsules?",
        "expected_result": [{"avg_daily_capsule_sales_percentage": 3.930574395721002}]
    },
    {

        "query": """ WITH ChannelSales AS (
           -- Facebook Channel
           SELECT
               SUM(acq_gross_revenue + rep_gross_revenue) AS total_revenue,
               SUM(acq_quantity + rep_quantity) AS total_orders,
               'Facebook' AS channel
           FROM products
           WHERE FB_Acq_Spend > 0 OR FB_Repeat_Spend > 0
        
           UNION ALL
        
           -- Affiliate Channel
           SELECT
               SUM(acq_gross_revenue + rep_gross_revenue) AS total_revenue,
               SUM(acq_quantity + rep_quantity) AS total_orders,
               'Affiliate' AS channel
           FROM products
           WHERE Aff_New_Spend > 0 OR Aff_Repeat_Spend > 0
        
           UNION ALL
        
           -- Influencer Channel
           SELECT
               SUM(acq_gross_revenue + rep_gross_revenue) AS total_revenue,
               SUM(acq_quantity + rep_quantity) AS total_orders,
               'Influencer' AS channel
           FROM products
           WHERE acq_influencer_spend > 0 OR repeat_influencer_spend > 0
        
           UNION ALL
        
           -- Content Marketing Channel
           SELECT
               SUM(acq_gross_revenue + rep_gross_revenue) AS total_revenue,
               SUM(acq_quantity + rep_quantity) AS total_orders,
               'Content Marketing' AS channel
           FROM products
           WHERE acq_content_marketing_spend > 0 OR repeat_content_marketing_spend > 0
        
           UNION ALL
        
           -- Partnership Channel
           SELECT
               SUM(acq_gross_revenue + rep_gross_revenue) AS total_revenue,
               SUM(acq_quantity + rep_quantity) AS total_orders,
               'Partnership' AS channel
           FROM products
           WHERE Partnership_New_spend > 0 OR Partnership_Repeat_spend > 0
        
           UNION ALL
        
           -- Google Advertising Channel
           SELECT
               SUM(acq_gross_revenue + rep_gross_revenue) AS total_revenue,
               SUM(acq_quantity + rep_quantity) AS total_orders,
               'Google Advertising' AS channel
           FROM products
           WHERE google_acq_spend > 0 OR google_repeat_spend > 0
        
           UNION ALL
        
           -- CRM Channel
           SELECT
               SUM(acq_gross_revenue + rep_gross_revenue) AS total_revenue,
               SUM(acq_quantity + rep_quantity) AS total_orders,
               'CRM' AS channel
           FROM products
           WHERE crm_new_spend > 0 OR crm_repeat_spend > 0
           -- Add similar blocks for other channels as needed
        )
        
        SELECT
           channel,
           (total_revenue / total_orders) AS AOV
        FROM ChannelSales
        ORDER BY AOV DESC
        LIMIT 1;
            """,
        "explanation": """Identify the marketing channel with the highest average order value (AOV).""",
        "expected_result": [{"channel": "Facebook"}, {"AOV": 1188.677100088054}]
    },
    {
        "query": """WITH ChannelAcquisitionSpend AS (
    -- Facebook Channel
    SELECT 
        SUM(FB_Acq_Spend) AS total_acq_spend,
        'Facebook' AS channel
    FROM products

    UNION ALL

    -- Affiliate Channel
    SELECT 
        SUM(Aff_New_Spend) AS total_acq_spend,
        'Affiliate' AS channel
    FROM products

    UNION ALL

    -- Influencer Channel
    SELECT 
        SUM(acq_influencer_spend) AS total_acq_spend,
        'Influencer' AS channel
    FROM products

    UNION ALL

    -- Content Marketing Channel
    SELECT 
        SUM(acq_content_marketing_spend) AS total_acq_spend,
        'Content Marketing' AS channel
    FROM products

    UNION ALL

    -- Partnership Channel
    SELECT 
        SUM(Partnership_New_spend) AS total_acq_spend,
        'Partnership' AS channel
    FROM products

    UNION ALL

    -- Google Advertising Channel
    SELECT 
        SUM(google_acq_spend) AS total_acq_spend,
        'Google Advertising' AS channel
    FROM products

    UNION ALL

    -- CRM Channel
    SELECT 
        SUM(crm_new_spend) AS total_acq_spend,
        'CRM' AS channel
    FROM products
    -- Add similar blocks for other channels as needed
)

SELECT 
    channel,
    total_acq_spend
FROM ChannelAcquisitionSpend
ORDER BY total_acq_spend DESC
LIMIT 1;
""",
        "explanation": """Determine the marketing channel with the most expenditure for acquiring orders.""",
        "expected_result": [{"channel": "Facebook"}, {"total_acq_spend": 4089882.8800000004}]
    },
    {

        "query": """WITH ProductRS AS (
    SELECT 
        name,
        (acq_net_revenue + rep_net_revenue) AS total_net_revenue,
        (
            FB_Acq_Spend + 
            Aff_New_Spend + 
            acq_influencer_spend + 
            acq_content_marketing_spend + 
            Partnership_New_spend + 
            google_acq_spend + 
            crm_new_spend +
            doc_new_spend +
            hct_acq_final_spend +
            acq_non_working_spend
            -- Add other acquisition spends as needed
        ) AS total_acq_spend
    FROM products
    WHERE therapy = 'Mens Health'
)

SELECT 
    name,
    (total_net_revenue / NULLIF(total_acq_spend, 0)) AS RS -- NULLIF to handle division by zero
FROM ProductRS
ORDER BY RS DESC
LIMIT 1;
""",
        "explanation": """Identify the product in the 'Men's Health' category that has the highest Return on Spend (R/S) ratio.""",
        "expected_result": [{"name": "KAPIVA HIMALAYA SHILAJIT 10 GRMS_UMA"}, {"RS": 108.48734989712052}]
    },
    {

        "query": """SELECT 
                        SUM(acq_gross_revenue + rep_gross_revenue) / NULLIF(SUM(acq_quantity + rep_quantity), 0) AS avg_product_value
                    FROM products
                    WHERE DATE(date_created) = '2023-07-28';
""",
    "explanation": """Calculate the average value of all products sold on July 28th, 2023.""",
        "expected_result": [{"avg_product_value": 1108.0539163179917}]
    },

    {

        "query": """WITH VeganProteinSales AS (
    SELECT 
        SUM(acq_net_revenue + rep_net_revenue) AS vegan_protein_revenue
    FROM products
    WHERE name LIKE '%vegan protein%'
),

TotalSales AS (
    SELECT 
        SUM(acq_net_revenue + rep_net_revenue) AS total_revenue
    FROM products
)

SELECT 
    (vegan_protein_revenue / NULLIF(total_revenue, 0)) * 100 AS vegan_protein_sales_percentage
FROM VeganProteinSales, TotalSales;
""",
"explanation": """Calculate the percentage of sales, across all time, that are attributed to vegan protein products when compared to the total sales.
""",
        "expected_result": [{"vegan_protein_sales_percentage": 0.5703014487057498}]
    },
    {
        "query": """WITH VeganProteinRS AS (
    SELECT 
        SUM(acq_net_revenue + rep_net_revenue) AS vegan_protein_revenue,
        SUM(
            FB_Acq_Spend + FB_Repeat_Spend + 
            Aff_New_Spend + Aff_Repeat_Spend + 
            acq_influencer_spend + repeat_influencer_spend + 
            acq_content_marketing_spend + repeat_content_marketing_spend + 
            Partnership_New_spend + Partnership_Repeat_spend + 
            google_acq_spend + google_repeat_spend + 
            crm_new_spend + crm_repeat_spend +
            doc_new_spend + doc_rep_spend +
            hct_acq_final_spend + hct_repeat_final_spend +
            acq_non_working_spend + repeat_non_working_spend
            -- Add other spends as needed
        ) AS total_spend
    FROM products
    WHERE name LIKE '%vegan protein%'
)

SELECT 
    (vegan_protein_revenue / NULLIF(total_spend, 0)) AS RS
FROM VeganProteinRS;
""",
"explanation": """Determine the Return on Spend (R/S) ratio for vegan protein products over all time periods.""",
        "expected_result": [{"RS": 13.296728656088307}]
    },
    {

        "query": """WITH WeekdaySales AS (
    SELECT 
        AVG(acq_net_revenue + rep_net_revenue) AS avg_weekday_sales,
        AVG(
            (acq_net_revenue + rep_net_revenue) - 
            (acq_cogs + rep_cogs) - 
            (acq_logs + rep_logs) - 
            (hct_acq_final_spend + hct_repeat_final_spend + doc_new_spend + doc_rep_spend + FB_Acq_Spend + FB_Repeat_Spend + Aff_New_Spend + Aff_Repeat_Spend + Partnership_New_spend + Partnership_Repeat_spend + google_acq_spend + google_repeat_spend + crm_new_spend + crm_repeat_spend) - 
            (acq_influencer_spend + repeat_influencer_spend + acq_content_marketing_spend + repeat_content_marketing_spend + acq_non_working_spend + repeat_non_working_spend)
        ) AS avg_weekday_cm3
    FROM products
    WHERE name LIKE '%Shilajit%' AND DAYOFWEEK(date_created) BETWEEN 2 AND 6
),

WeekendSales AS (
    SELECT 
        AVG(acq_net_revenue + rep_net_revenue) AS avg_weekend_sales,
        AVG(
            (acq_net_revenue + rep_net_revenue) - 
            (acq_cogs + rep_cogs) - 
            (acq_logs + rep_logs) - 
            (hct_acq_final_spend + hct_repeat_final_spend + doc_new_spend + doc_rep_spend + FB_Acq_Spend + FB_Repeat_Spend + Aff_New_Spend + Aff_Repeat_Spend + Partnership_New_spend + Partnership_Repeat_spend + google_acq_spend + google_repeat_spend + crm_new_spend + crm_repeat_spend) - 
            (acq_influencer_spend + repeat_influencer_spend + acq_content_marketing_spend + repeat_content_marketing_spend + acq_non_working_spend + repeat_non_working_spend)
        ) AS avg_weekend_cm3
    FROM products
    WHERE name LIKE '%Shilajit%' AND DAYOFWEEK(date_created) IN (1, 7)
)

SELECT 
    ((avg_weekend_sales - avg_weekday_sales) / NULLIF(avg_weekday_sales, 0)) * 100 AS sales_percentage_increase,
    ((avg_weekend_cm3 - avg_weekday_cm3) / NULLIF(avg_weekday_cm3, 0)) * 100 AS cm3_percentage_change
FROM WeekdaySales, WeekendSales;
""",
        "explanation": """Calculate the percentage increase in sales of Shilajit products during weekends compared to weekdays. Additionally, determine the change in Contribution Margin 3 (CM3) alongside this sales change.""",
        "expected_result": [{"sales_percentage_increase": -10.232938942790856},
                            {"cm3_percentage_change": -38.60571972902224}]
    },
    {

        "query": """WITH WeekdayImpact AS (
    SELECT 
        SUM(acq_mrp_revenue + rep_mrp_revenue) * 0.05 AS potential_weekday_increase
    FROM products
    WHERE name LIKE '%Shilajit Gold%' AND DAYOFWEEK(date_created) BETWEEN 2 AND 6
),

WeekendImpact AS (
    SELECT 
        SUM(acq_mrp_revenue + rep_mrp_revenue) * 0.05 AS potential_weekend_increase
    FROM products
    WHERE name LIKE '%Shilajit Gold%' AND DAYOFWEEK(date_created) IN (1, 7)
)

SELECT 
    potential_weekday_increase,
    potential_weekend_increase
FROM WeekdayImpact, WeekendImpact;
""",
"explanation": """Estimate the potential increase in sales revenue for 'Shilajit Gold' products due to a 5% decrease in discount, considering both weekdays and weekends separately.""",
"expected_result": [{"average_daily_quantity": 1269.6250}, {"capsule_sales": 689613.4329365998}, {"percentage_capsule_sales": 4.019939802966768}]
    },
    # add more examples here
]
