#!/usr/bin/env python3
"""
XYZ Education — TCO Calculator
Bottom-up cost model for AWS, Azure, GCP, and Canonical Private Cloud.
All prices are for ap-southeast-1 (Singapore) region, 3-year Reserved/CUD.
Prices sourced from public pricing pages as of Q1 2026.
"""

# ============================================================
# INFRASTRUCTURE MODEL (from xyz_infrastructure_model.md)
# ============================================================

workloads = {
    "Video Transcoding": {
        "vcpus_per_instance": 16,
        "ram_gb": 32,
        "count": 2540,
        "total_vcpus": 2540 * 16,  # 40,640
        "aws_type": "c7i.4xlarge",
        "azure_type": "F16s v2",
        "gcp_type": "c2-standard-16",
    },
    "Media/WebRTC": {
        "vcpus_per_instance": 8,
        "ram_gb": 16,
        "count": 800,
        "total_vcpus": 800 * 8,  # 6,400
        "aws_type": "c7i.2xlarge",
        "azure_type": "F8s v2",
        "gcp_type": "c2-standard-8",
    },
    "App/API": {
        "vcpus_per_instance": 8,
        "ram_gb": 32,
        "count": 400,
        "total_vcpus": 400 * 8,  # 3,200
        "aws_type": "m7i.2xlarge",
        "azure_type": "D8s v5",
        "gcp_type": "e2-standard-8",
    },
    "Database": {
        "vcpus_per_instance": 16,
        "ram_gb": 128,
        "count": 150,
        "total_vcpus": 150 * 16,  # 2,400
        "aws_type": "r7i.4xlarge",
        "azure_type": "E16s v5",
        "gcp_type": "n2-highmem-16",
    },
    "AI Inference": {
        "vcpus_per_instance": 16,
        "ram_gb": 32,
        "count": 125,
        "total_vcpus": 125 * 16,  # 2,000
        "aws_type": "c7i.4xlarge",
        "azure_type": "F16s v2",
        "gcp_type": "c2-standard-16",
    },
}

# ============================================================
# PRICING: AWS (ap-southeast-1, 3yr Reserved All Upfront)
# Source: https://aws.amazon.com/ec2/pricing/reserved-instances/
# ============================================================

aws_hourly_ri_3yr = {
    # 3yr All Upfront effective hourly rate (ap-southeast-1)
    "c7i.4xlarge": 0.312,   # Compute optimized, 16 vCPU, 32GB
    "c7i.2xlarge": 0.156,   # 8 vCPU, 16GB
    "m7i.2xlarge": 0.183,   # General purpose, 8 vCPU, 32GB
    "r7i.4xlarge": 0.464,   # Memory optimized, 16 vCPU, 128GB
}

# Storage
aws_ebs_gp3_per_gb_month = 0.088      # $/GB/month (ap-southeast-1)
aws_s3_per_gb_month = 0.025            # $/GB/month (first 50TB tier, ap-southeast-1)
aws_egress_per_gb = 0.09              # $/GB (ap-southeast-1, after first 10TB)

# ============================================================
# PRICING: Azure (Southeast Asia, 3yr Reserved)
# Source: https://azure.microsoft.com/pricing/details/virtual-machines/
# ============================================================

azure_hourly_ri_3yr = {
    "F16s v2": 0.278,     # Compute optimized, 16 vCPU, 32GB
    "F8s v2": 0.139,      # 8 vCPU, 16GB
    "D8s v5": 0.175,      # General purpose, 8 vCPU, 32GB
    "E16s v5": 0.428,     # Memory optimized, 16 vCPU, 128GB
}

azure_disk_per_gb_month = 0.088        # Premium SSD P30 equivalent
azure_blob_per_gb_month = 0.020        # Hot tier
azure_egress_per_gb = 0.087            # Bandwidth pricing

# ============================================================
# PRICING: GCP (asia-southeast1, 3yr CUD)
# Source: https://cloud.google.com/compute/vm-instance-pricing
# ============================================================

gcp_hourly_cud_3yr = {
    "c2-standard-16": 0.295,   # Compute optimized, 16 vCPU, 64GB
    "c2-standard-8": 0.148,    # 8 vCPU, 32GB
    "e2-standard-8": 0.120,    # General purpose, 8 vCPU, 32GB
    "n2-highmem-16": 0.420,    # High memory, 16 vCPU, 128GB
}

gcp_pd_per_gb_month = 0.088           # SSD Persistent Disk
gcp_gcs_per_gb_month = 0.020          # Standard Storage
gcp_egress_per_gb = 0.12              # Premium tier egress

# ============================================================
# CANONICAL PRIVATE CLOUD (from Pricing Report 2022)
# ============================================================

canonical_hardware_capex = 8_800_000   # $8.8M for ~500 bare-metal servers
canonical_managed_opex_yr = 3_200_000  # $3.2M/year Fully Managed Service

# ============================================================
# STORAGE & NETWORK CONSTANTS
# ============================================================

block_storage_tb = 500                 # TB of block/SSD storage
object_storage_pb = 5                  # PB of archival object storage
object_storage_tb = object_storage_pb * 1000  # 5,000 TB
monthly_egress_pb = 1.5               # PB/month outbound
monthly_egress_tb = monthly_egress_pb * 1000  # 1,500 TB
monthly_egress_gb = monthly_egress_tb * 1000  # 1,500,000 GB

HOURS_PER_YEAR = 8760
HOURS_3YR = HOURS_PER_YEAR * 3


def calc_cloud_cost(hourly_prices, workloads_map, type_key,
                    ebs_rate, s3_rate, egress_rate):
    """Calculate 3-year total for a cloud provider."""

    # --- Compute ---
    compute_yearly = 0
    compute_detail = {}
    for name, w in workloads.items():
        inst_type = w[type_key]
        rate = hourly_prices[inst_type]
        yearly = w["count"] * rate * HOURS_PER_YEAR
        compute_detail[name] = yearly
        compute_yearly += yearly

    compute_3yr = compute_yearly * 3

    # --- Storage ---
    block_yearly = block_storage_tb * 1000 * ebs_rate * 12     # TB→GB, $/GB/mo × 12
    object_yearly = object_storage_tb * 1000 * s3_rate * 12    # TB→GB
    storage_3yr = (block_yearly + object_yearly) * 3

    # --- Egress ---
    egress_yearly = monthly_egress_gb * egress_rate * 12
    egress_3yr = egress_yearly * 3

    total_3yr = compute_3yr + storage_3yr + egress_3yr

    return {
        "compute_yearly": compute_yearly,
        "compute_3yr": compute_3yr,
        "compute_detail": compute_detail,
        "block_yearly": block_yearly,
        "object_yearly": object_yearly,
        "storage_3yr": storage_3yr,
        "egress_yearly": egress_yearly,
        "egress_3yr": egress_3yr,
        "total_yearly": compute_yearly + block_yearly + object_yearly + egress_yearly,
        "total_3yr": total_3yr,
    }


def calc_canonical():
    """Calculate 3-year total for Canonical Managed Private Cloud."""
    total_3yr = canonical_hardware_capex + (canonical_managed_opex_yr * 3)
    return {
        "hardware": canonical_hardware_capex,
        "managed_yearly": canonical_managed_opex_yr,
        "managed_3yr": canonical_managed_opex_yr * 3,
        "total_3yr": total_3yr,
    }


def fmt(n):
    """Format number as $X.XM"""
    return f"${n / 1_000_000:.1f}M"


def main():
    # Total vCPUs
    total_vcpus = sum(w["total_vcpus"] for w in workloads.values())
    total_instances = sum(w["count"] for w in workloads.values())

    print("=" * 72)
    print("XYZ EDUCATION — 3-YEAR TCO ANALYSIS")
    print("=" * 72)
    print(f"\nTotal vCPUs: {total_vcpus:,}")
    print(f"Total Instances: {total_instances:,}")
    print(f"Block Storage: {block_storage_tb} TB | Object Storage: {object_storage_pb} PB")
    print(f"Monthly Egress: {monthly_egress_pb} PB ({monthly_egress_gb:,.0f} GB)")

    print("\n" + "-" * 72)
    print("WORKLOAD BREAKDOWN")
    print("-" * 72)
    for name, w in workloads.items():
        pct = w["total_vcpus"] / total_vcpus * 100
        print(f"  {name:25s} | {w['count']:>5,} instances | "
              f"{w['total_vcpus']:>6,} vCPUs ({pct:.0f}%)")

    # AWS
    aws = calc_cloud_cost(aws_hourly_ri_3yr, workloads, "aws_type",
                          aws_ebs_gp3_per_gb_month, aws_s3_per_gb_month,
                          aws_egress_per_gb)

    # Azure
    azure = calc_cloud_cost(azure_hourly_ri_3yr, workloads, "azure_type",
                            azure_disk_per_gb_month, azure_blob_per_gb_month,
                            azure_egress_per_gb)

    # GCP
    gcp = calc_cloud_cost(gcp_hourly_cud_3yr, workloads, "gcp_type",
                          gcp_pd_per_gb_month, gcp_gcs_per_gb_month,
                          gcp_egress_per_gb)

    # Canonical
    canonical = calc_canonical()

    # Print Results
    for provider, data, color in [
        ("AWS (ap-southeast-1)", aws, ""),
        ("Azure (Southeast Asia)", azure, ""),
        ("GCP (asia-southeast1)", gcp, ""),
    ]:
        print(f"\n{'=' * 72}")
        print(f"  {provider} — 3-Year Reserved / CUD")
        print(f"{'=' * 72}")
        print(f"  Compute (yearly):  {fmt(data['compute_yearly']):>10}")
        for name, cost in data["compute_detail"].items():
            print(f"    └─ {name:23s}  {fmt(cost):>10}")
        print(f"  Block Storage (yearly): {fmt(data['block_yearly']):>10}")
        print(f"  Object Storage (yearly): {fmt(data['object_yearly']):>10}")
        print(f"  Egress (yearly):   {fmt(data['egress_yearly']):>10}")
        print(f"  ─────────────────────────────────────")
        print(f"  YEARLY TOTAL:      {fmt(data['total_yearly']):>10}")
        print(f"  ═══════════════════════════════════════")
        print(f"  3-YEAR TOTAL:      {fmt(data['total_3yr']):>10}")

    print(f"\n{'=' * 72}")
    print(f"  CANONICAL (Managed Private Cloud)")
    print(f"{'=' * 72}")
    print(f"  Hardware CapEx:    {fmt(canonical['hardware']):>10}")
    print(f"  Managed OPEX (yearly): {fmt(canonical['managed_yearly']):>10}")
    print(f"  Managed OPEX (3yr):    {fmt(canonical['managed_3yr']):>10}")
    print(f"  ═══════════════════════════════════════")
    print(f"  3-YEAR TOTAL:      {fmt(canonical['total_3yr']):>10}")

    # Comparison Summary
    print(f"\n{'=' * 72}")
    print(f"  FINAL COMPARISON — 3-YEAR TCO")
    print(f"{'=' * 72}")
    print(f"  AWS:       {fmt(aws['total_3yr']):>10}")
    print(f"  Azure:     {fmt(azure['total_3yr']):>10}")
    print(f"  GCP:       {fmt(gcp['total_3yr']):>10}")
    print(f"  Canonical: {fmt(canonical['total_3yr']):>10}")
    print(f"  ─────────────────────────────────────")

    savings_aws = aws['total_3yr'] - canonical['total_3yr']
    savings_azure = azure['total_3yr'] - canonical['total_3yr']
    savings_gcp = gcp['total_3yr'] - canonical['total_3yr']
    print(f"  Savings vs AWS:   {fmt(savings_aws):>10} ({savings_aws/aws['total_3yr']*100:.0f}%)")
    print(f"  Savings vs Azure: {fmt(savings_azure):>10} ({savings_azure/azure['total_3yr']*100:.0f}%)")
    print(f"  Savings vs GCP:   {fmt(savings_gcp):>10} ({savings_gcp/gcp['total_3yr']*100:.0f}%)")
    print()


if __name__ == "__main__":
    main()
