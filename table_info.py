custom_table_info={"products":
                       """CREATE TABLE products (
                                        "date_created" DATETIME,
                                        "name" TEXT,
                                        "therapy" TEXT,
                                        "group" TEXT,
                                        "type" TEXT,
                                        "acq_mrp_revenue" DOUBLE,
                                        "rep_mrp_revenue" DOUBLE,
                                        "acq_item_discount" DOUBLE,
                                        "rep_item_discount" DOUBLE,
                                        "acq_listing_discount_uc" DOUBLE,
                                        "rep_listing_discount_uc" DOUBLE,
                                        "acq_gross_revenue" DOUBLE,
                                        "rep_gross_revenue" DOUBLE,
                                        "acq_net_revenue" DOUBLE,
                                        "rep_net_revenue" DOUBLE,
                                        "acq_quantity" INTEGER,
                                        "rep_quantity" INTEGER,
                                        "acq_cogs" DOUBLE,
                                        "rep_cogs" DOUBLE,
                                        "acq_logs" DOUBLE,
                                        "rep_logs" DOUBLE,
                                        "hct_acq_final_spend" DOUBLE,
                                        "hct_repeat_final_spend" DOUBLE,
                                        "doc_new_spend" DOUBLE,
                                        "doc_rep_spend" DOUBLE,
                                        "acq_influencer_spend" DOUBLE,
                                        "repeat_influencer_spend" DOUBLE,
                                        "acq_content_marketing_spend" DOUBLE,
                                        "repeat_content_marketing_spend" DOUBLE,
                                        "FB_Acq_Spend" DOUBLE,
                                        "FB_Repeat_Spend" DOUBLE,
                                        "Aff_New_Spend" DOUBLE,
                                        "Aff_Repeat_Spend" DOUBLE,
                                        "Partnership_New_spend" DOUBLE,
                                        "Partnership_Repeat_spend" DOUBLE,
                                        "acq_non_working_spend" DOUBLE,
                                        "repeat_non_working_spend" DOUBLE,
                                        "google_acq_spend" DOUBLE,
                                        "google_repeat_spend" DOUBLE,
                                        "crm_new_spend" DOUBLE,
                                        "crm_repeat_spend" DOUBLE
                                        )

/*
3 rows from products table:
date_created	name	therapy	group	type	acq_mrp_revenue	rep_mrp_revenue	acq_item_discount	rep_item_discount	acq_listing_discount_uc	rep_listing_discount_uc	acq_gross_revenue	rep_gross_revenue	acq_net_revenue	rep_net_revenue	acq_quantity	rep_quantity	acq_cogs	rep_cogs	acq_logs	rep_logs	hct_acq_final_spend	hct_repeat_final_spend	doc_new_spend	doc_rep_spend	acq_influencer_spend	repeat_influencer_spend	acq_content_marketing_spend	repeat_content_marketing_spend	FB_Acq_Spend	FB_Repeat_Spend	Aff_New_Spend	Aff_Repeat_Spend	Partnership_New_spend	Partnership_Repeat_spend	acq_non_working_spend	repeat_non_working_spend	google_acq_spend	google_repeat_spend	crm_new_spend	crm_repeat_spend
2023-07-15 00:00:00	KAPIVA HIMALAYA SHILAJIT 20 GRMS_UMA	Mens Health	HPC	Ingestibles	812458.0000000000	317788.0000000000	29943.8100000000	11730.5200000000	260567.4600000000	106414.3700000000	462203.0700000000	165014.1100000000	348620.1767000000	121610.6862000000	438	164	87416.0400000000	32731.1200000000	16058.1180300000	5178.0363120000	16582.9640200000	11904.7665200000	1530.4529580000	259.1257546000	0E-10	0E-10	0E-10	0E-10	193636.8000000000	48409.2000000000	17522.0917100000	4806.5613650000	14474.2355000000	3201.9048000000	7952.0000000000	1988.0000000000	38661.5200000000	9665.3800000000	0E-10	1446.8768130000
2023-07-15 00:00:00	KAPIVA HIM FOODS SHILAJIT GOLD RESIN - 20G	Mens Health	HPC	Ingestibles	304031.0000000000	221277.0000000000	18037.0000000000	14885.0000000000	64343.0000000000	54066.0000000000	204361.0000000000	143713.0000000000	151321.5100000000	113518.0500000000	140	109	35435.4000000000	27588.9900000000	4613.1114620000	2784.1052820000	6662.0877010000	6124.0523000000	343.7716898000	929.1938266000	0E-10	0E-10	0E-10	0E-10	69626.4000000000	17406.6000000000	9313.3902930000	3137.2229570000	3829.1370000000	1181.6130500000	14145.6000000000	3536.4000000000	24823.3600000000	6205.8400000000	1569.8825230000	0E-10
2023-07-15 00:00:00	KAPIVA HIMALAYA SHILAJIT 30 GRAMS	Mens Health	HPC	Ingestibles	102851.0000000000	18891.0000000000	4165.0000000000	648.0000000000	33150.0000000000	6863.0000000000	56453.0000000000	10530.0000000000	42424.7600000000	8839.0500000000	39	8	10733.9700000000	2201.8400000000	1745.3520000000	313.8668000000	0E-10	0E-10	589.7909705000	0E-10	0E-10	0E-10	0E-10	0E-10	0E-10	0E-10	1996.5259360000	207.5743673000	1644.4855000000	0E-10	0E-10	0E-10	0E-10	0E-10	0E-10	0E-10
*/
"""}
table_info="""acq_mrp_revenue: Revenue generated from new customer acquisitions (acq) based on the maximum retail price (MRP).
rep_mrp_revenue: Revenue generated from repeat customers (rep) based on the maximum retail price (MRP).
acq_item_discount: Discount provided to new customers (acq) on individual items.
rep_item_discount: Discount provided to repeat customers (rep) on individual items.
acq_listing_discount_uc: Listing discount for new customer acquisitions (acq) in unconverted currency.
rep_listing_discount_uc: Listing discount for repeat customers (rep) in unconverted currency.
acq_gross_revenue: Gross revenue from new customer acquisitions (acq).
rep_gross_revenue: Gross revenue from repeat customers (rep).
acq_net_revenue: Net revenue from new customer acquisitions (acq).
rep_net_revenue: Net revenue from repeat customers (rep).
acq_quantity: Quantity of products sold to new customers (acq).
rep_quantity: Quantity of products sold to repeat customers (rep).
acq_cogs: Cost of goods sold for new customer acquisitions (acq).
rep_cogs: Cost of goods sold for repeat customers (rep).
acq_logs: Logs related to new customer acquisitions (acq).
rep_logs: Logs related to repeat customers (rep).
hct_acq_final_spend: Final spend for new customer acquisitions (acq) related to hct (unclear abbreviation).
hct_repeat_final_spend: Final spend for repeat customers (rep) related to hct (unclear abbreviation).
doc_new_spend: New spend on doctor-related activities for new customers (acq).
doc_rep_spend: Spend on doctor-related activities for repeat customers (rep).
acq_influencer_spend: Spend on influencers for new customer acquisitions (acq).
repeat_influencer_spend: Spend on influencers for repeat customers (rep).
acq_content_marketing_spend: Spend on content marketing for new customer acquisitions (acq).
repeat_content_marketing_spend: Spend on content marketing for repeat customers (rep).
FB_Acq_Spend: Spend on Facebook advertising for new customer acquisitions (acq).
FB_Repeat_Spend: Spend on Facebook advertising for repeat customers (rep).
Aff_New_Spend: Spend on affiliate marketing for new customer acquisitions (acq).
Aff_Repeat_Spend: Spend on affiliate marketing for repeat customers (rep).
Partnership_New_spend: Spend on partnerships for new customer acquisitions (acq).
Partnership_Repeat_spend: Spend on partnerships for repeat customers (rep).
acq_non_working_spend: Non-working spend for new customer acquisitions (acq).
repeat_non_working_spend: Non-working spend for repeat customers (rep).
google_acq_spend: Spend on Google advertising for new customer acquisitions (acq).
google_repeat_spend: Spend on Google advertising for repeat customers (rep).
crm_new_spend: Spend on customer relationship management for new customer acquisitions (acq).
crm_repeat_spend: Spend on customer relationship management for repeat customers (rep)."""