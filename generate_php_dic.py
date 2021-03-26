import os
import json
import pandas as pd
# genotypes
genotype_tables = ["clin_table", "mRNA_table", "splicing_table", "mutaiton_table", "methylation_table", "copy_number_table"]
#import tissue configuration file
primary_site_df = pd.read_csv("tcga_cancers_primary_site.csv")
#find all cancer types from tissue configuration file
cancer_types = primary_site_df["cancer_type"].unique().tolist()
#convert the file to dict
primary_site_dict = primary_site_df .groupby('primary_site')['cancer_type'].apply(list).to_dict()


cancer_dict = dict()
for x in cancer_types:
    inner_dict = dict()
    for y in genotype_tables:
        inner_dict[y] = x+"_"+y
    cancer_dict[x] = inner_dict

full_dict = dict()
for key, value in primary_site_dict.items():
    inner = dict()
    for k, v in cancer_dict.items():
        if k in value:
            inner[k] = v
    full_dict[key] = inner


print(json.dumps(full_dict))
