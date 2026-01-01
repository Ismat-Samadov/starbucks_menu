"""
Starbucks Menu Analysis - Chart Generation Script
Generates business-focused visualizations for strategic decision-making
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set professional styling
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11

# Load and clean data
df = pd.read_csv('starbucks.csv')

# Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

# Convert percentage columns to numeric
percentage_cols = ['Vitamin A (% DV)', 'Vitamin C (% DV)', 'Calcium (% DV)', 'Iron (% DV)']
for col in percentage_cols:
    df[col] = df[col].str.rstrip('%').replace('', '0').astype(float)

# Handle Caffeine column
df['Caffeine (mg)'] = pd.to_numeric(df['Caffeine (mg)'], errors='coerce')

# Extract size information
size_order = ['Short', 'Tall', 'Grande', 'Venti']
df['Size'] = df['Beverage_prep'].apply(lambda x: next((s for s in size_order if s in str(x)), 'Other'))

# Extract milk type
milk_types = ['Nonfat Milk', '2% Milk', 'Soymilk', 'Whole Milk']
df['Milk_Type'] = df['Beverage_prep'].apply(lambda x: next((m for m in milk_types if m in str(x)), 'No Milk'))

print("Generating business insights charts...")
print("=" * 80)


# ============================================================================
# CHART 1: Revenue Opportunity - Calorie Distribution by Category
# ============================================================================
print("Chart 1: Category Performance Analysis (Calories by Category)")
plt.figure(figsize=(14, 7))
category_calories = df.groupby('Beverage_category')['Calories'].agg(['mean', 'min', 'max']).sort_values('mean', ascending=False)

x = np.arange(len(category_calories))
width = 0.6

bars = plt.bar(x, category_calories['mean'], width, color='#00704A', alpha=0.8, label='Average Calories')
plt.errorbar(x, category_calories['mean'],
             yerr=[category_calories['mean'] - category_calories['min'],
                   category_calories['max'] - category_calories['mean']],
             fmt='none', ecolor='#333333', capsize=5, alpha=0.6)

plt.xlabel('Beverage Category', fontweight='bold')
plt.ylabel('Calories', fontweight='bold')
plt.title('Menu Portfolio Analysis: Average Calories by Category\n(Error bars show min-max range)',
          fontweight='bold', fontsize=14)
plt.xticks(x, category_calories.index, rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/01_category_calorie_analysis.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================================
# CHART 2: Health Trend Analysis - Sugar Content by Category
# ============================================================================
print("Chart 2: Health Positioning - Sugar Content Analysis")
plt.figure(figsize=(14, 7))
sugar_data = df.groupby('Beverage_category')['Sugars (g)'].agg(['mean', 'median']).sort_values('mean', ascending=False)

x = np.arange(len(sugar_data))
width = 0.35

plt.bar(x - width/2, sugar_data['mean'], width, label='Average Sugar', color='#D62B1F', alpha=0.8)
plt.bar(x + width/2, sugar_data['median'], width, label='Median Sugar', color='#FDB913', alpha=0.8)

plt.xlabel('Beverage Category', fontweight='bold')
plt.ylabel('Sugar Content (grams)', fontweight='bold')
plt.title('Health Impact Assessment: Sugar Content Across Product Lines\n(Higher values indicate less health-conscious positioning)',
          fontweight='bold', fontsize=14)
plt.xticks(x, sugar_data.index, rotation=45, ha='right')
plt.legend(loc='upper right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/02_sugar_content_analysis.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================================
# CHART 3: Customer Segmentation - Size Impact on Calories
# ============================================================================
print("Chart 3: Customer Behavior - Size Selection Impact")
plt.figure(figsize=(12, 6))
size_data = df[df['Size'].isin(size_order)].groupby('Size')['Calories'].mean().reindex(size_order)

colors = ['#1E3932', '#00704A', '#00A862', '#6FCDAA']
bars = plt.bar(range(len(size_data)), size_data.values, color=colors, alpha=0.85)

# Add value labels on bars
for i, (idx, val) in enumerate(size_data.items()):
    plt.text(i, val + 5, f'{val:.0f}', ha='center', fontweight='bold', fontsize=11)

plt.xlabel('Size', fontweight='bold')
plt.ylabel('Average Calories', fontweight='bold')
plt.title('Upselling Opportunity: Calorie Increase by Size Upgrade\n(Indicates potential for larger portion sales)',
          fontweight='bold', fontsize=14)
plt.xticks(range(len(size_data)), size_data.index)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/03_size_impact_analysis.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================================
# CHART 4: Product Differentiation - Caffeine Content
# ============================================================================
print("Chart 4: Product Positioning - Caffeine Levels")
plt.figure(figsize=(14, 7))
caffeine_data = df[df['Caffeine (mg)'].notna() & (df['Caffeine (mg)'] > 0)].groupby('Beverage_category')['Caffeine (mg)'].mean().sort_values(ascending=False)

plt.barh(range(len(caffeine_data)), caffeine_data.values, color='#4E2A1E', alpha=0.8)
plt.yticks(range(len(caffeine_data)), caffeine_data.index)
plt.xlabel('Average Caffeine Content (mg)', fontweight='bold')
plt.ylabel('Beverage Category', fontweight='bold')
plt.title('Energy Positioning: Caffeine Content by Category\n(Critical for functional benefit marketing)',
          fontweight='bold', fontsize=14)

# Add value labels
for i, val in enumerate(caffeine_data.values):
    plt.text(val + 2, i, f'{val:.0f} mg', va='center', fontweight='bold')

plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/04_caffeine_positioning.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================================
# CHART 5: Milk Choice Impact - Fat and Calorie Comparison
# ============================================================================
print("Chart 5: Customization Analysis - Milk Type Impact")
plt.figure(figsize=(12, 6))

# Clean Total Fat column if needed
df['Total Fat (g)'] = pd.to_numeric(df['Total Fat (g)'], errors='coerce')
milk_data = df[df['Milk_Type'] != 'No Milk'].groupby('Milk_Type')[['Calories', 'Total Fat (g)']].mean()

x = np.arange(len(milk_data))
width = 0.35

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(x - width/2, milk_data['Calories'], width, label='Calories', color='#00704A', alpha=0.8)
ax1.set_xlabel('Milk Type', fontweight='bold')
ax1.set_ylabel('Average Calories', fontweight='bold', color='#00704A')
ax1.tick_params(axis='y', labelcolor='#00704A')
ax1.set_xticks(x)
ax1.set_xticklabels(milk_data.index)

ax2 = ax1.twinx()
ax2.bar(x + width/2, milk_data['Total Fat (g)'], width, label='Total Fat', color='#D62B1F', alpha=0.8)
ax2.set_ylabel('Average Total Fat (g)', fontweight='bold', color='#D62B1F')
ax2.tick_params(axis='y', labelcolor='#D62B1F')

plt.title('Customization Economics: Nutritional Impact of Milk Choices\n(Informs premium pricing and health-conscious positioning)',
          fontweight='bold', fontsize=14)

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/05_milk_type_impact.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================================
# CHART 6: Menu Complexity - Product Count by Category
# ============================================================================
print("Chart 6: Menu Optimization - Product Line Distribution")
plt.figure(figsize=(12, 6))
product_count = df.groupby('Beverage_category').size().sort_values(ascending=True)

plt.barh(range(len(product_count)), product_count.values, color='#00A862', alpha=0.8)
plt.yticks(range(len(product_count)), product_count.index)
plt.xlabel('Number of SKUs', fontweight='bold')
plt.ylabel('Beverage Category', fontweight='bold')
plt.title('Portfolio Complexity: SKU Count by Category\n(Identifies potential for menu simplification or expansion)',
          fontweight='bold', fontsize=14)

# Add value labels
for i, val in enumerate(product_count.values):
    plt.text(val + 0.5, i, str(val), va='center', fontweight='bold')

plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/06_product_portfolio_distribution.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================================
# CHART 7: Nutritional Balance - Protein vs Calories
# ============================================================================
print("Chart 7: Nutritional Value Proposition - Protein Content")
plt.figure(figsize=(14, 7))
protein_data = df.groupby('Beverage_category')['Protein (g)'].mean().sort_values(ascending=False)

bars = plt.bar(range(len(protein_data)), protein_data.values, color='#4E2A1E', alpha=0.8)

# Color code by protein level
colors_map = ['#D62B1F' if x < 5 else '#FDB913' if x < 10 else '#00704A' for x in protein_data.values]
for bar, color in zip(bars, colors_map):
    bar.set_color(color)
    bar.set_alpha(0.8)

plt.xlabel('Beverage Category', fontweight='bold')
plt.ylabel('Average Protein Content (g)', fontweight='bold')
plt.title('Nutritional Differentiation: Protein Levels Across Categories\n(Green: High protein (10g+) | Yellow: Medium (5-10g) | Red: Low (<5g))',
          fontweight='bold', fontsize=14)
plt.xticks(range(len(protein_data)), protein_data.index, rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/07_protein_nutrition_value.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================================
# CHART 8: Health Conscious Options - Low Calorie Product Availability
# ============================================================================
print("Chart 8: Health Trends - Low-Calorie Option Coverage")
plt.figure(figsize=(12, 6))

# Define low calorie threshold (under 150 calories)
low_cal_threshold = 150
category_analysis = df.groupby('Beverage_category').agg({
    'Calories': lambda x: (x < low_cal_threshold).sum() / len(x) * 100
}).sort_values('Calories', ascending=False)

bars = plt.barh(range(len(category_analysis)), category_analysis['Calories'].values, color='#00A862', alpha=0.8)

# Color code by percentage
for i, (val, bar) in enumerate(zip(category_analysis['Calories'].values, bars)):
    if val >= 50:
        bar.set_color('#00704A')
    elif val >= 25:
        bar.set_color('#FDB913')
    else:
        bar.set_color('#D62B1F')
    bar.set_alpha(0.8)
    plt.text(val + 1, i, f'{val:.1f}%', va='center', fontweight='bold')

plt.yticks(range(len(category_analysis)), category_analysis.index)
plt.xlabel('Percentage of Low-Calorie Options (<150 cal)', fontweight='bold')
plt.ylabel('Beverage Category', fontweight='bold')
plt.title('Health Positioning Strategy: Low-Calorie Product Penetration by Category\n(Green: Strong (50%+) | Yellow: Moderate (25-50%) | Red: Weak (<25%))',
          fontweight='bold', fontsize=14)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/08_low_calorie_coverage.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================================
# CHART 9: Sodium Content Analysis - Health Risk Assessment
# ============================================================================
print("Chart 9: Health Risk Analysis - Sodium Levels")
plt.figure(figsize=(14, 7))
sodium_data = df.groupby('Beverage_category')['Sodium (mg)'].agg(['mean', 'max']).sort_values('mean', ascending=False)

x = np.arange(len(sodium_data))
width = 0.35

plt.bar(x - width/2, sodium_data['mean'], width, label='Average Sodium', color='#00704A', alpha=0.8)
plt.bar(x + width/2, sodium_data['max'], width, label='Maximum Sodium', color='#D62B1F', alpha=0.8)

plt.xlabel('Beverage Category', fontweight='bold')
plt.ylabel('Sodium Content (mg)', fontweight='bold')
plt.title('Health Compliance Assessment: Sodium Levels by Category\n(Critical for health regulations and customer wellness concerns)',
          fontweight='bold', fontsize=14)
plt.xticks(x, sodium_data.index, rotation=45, ha='right')
plt.legend(loc='upper right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/09_sodium_health_risk.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================================
# CHART 10: Top 15 Highest Calorie Products - Risk Identification
# ============================================================================
print("Chart 10: Product Risk Assessment - Highest Calorie Items")
plt.figure(figsize=(12, 8))
top_cal = df.nlargest(15, 'Calories')[['Beverage', 'Beverage_prep', 'Calories']].copy()
top_cal['Label'] = top_cal['Beverage'].str[:25] + ' (' + top_cal['Beverage_prep'].str[:15] + ')'

plt.barh(range(len(top_cal)), top_cal['Calories'].values, color='#D62B1F', alpha=0.8)
plt.yticks(range(len(top_cal)), top_cal['Label'].values, fontsize=9)
plt.xlabel('Calories', fontweight='bold')
plt.ylabel('Product', fontweight='bold')
plt.title('Health Liability Assessment: Top 15 Highest-Calorie Products\n(Potential targets for reformulation or health disclaimers)',
          fontweight='bold', fontsize=14)

# Add value labels
for i, val in enumerate(top_cal['Calories'].values):
    plt.text(val + 5, i, str(val), va='center', fontweight='bold')

plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/10_highest_calorie_products.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================================
# CHART 11: Carbohydrate Distribution - Energy Source Analysis
# ============================================================================
print("Chart 11: Energy Profile - Carbohydrate Content")
plt.figure(figsize=(14, 7))
carb_data = df.groupby('Beverage_category')['Total Carbohydrates (g)'].mean().sort_values(ascending=False)

plt.bar(range(len(carb_data)), carb_data.values, color='#FDB913', alpha=0.8)
plt.xlabel('Beverage Category', fontweight='bold')
plt.ylabel('Average Carbohydrates (g)', fontweight='bold')
plt.title('Energy Delivery Analysis: Carbohydrate Levels by Category\n(Indicates quick energy delivery and satiety potential)',
          fontweight='bold', fontsize=14)
plt.xticks(range(len(carb_data)), carb_data.index, rotation=45, ha='right')

# Add value labels on bars
for i, val in enumerate(carb_data.values):
    plt.text(i, val + 1, f'{val:.1f}', ha='center', fontweight='bold', fontsize=9)

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/11_carbohydrate_energy_analysis.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================================
# CHART 12: Size Upgrade Revenue Potential
# ============================================================================
print("Chart 12: Revenue Optimization - Size Upgrade Opportunity")
plt.figure(figsize=(12, 6))

# Calculate size progression for popular categories
popular_categories = df['Beverage_category'].value_counts().head(5).index
size_progression = df[df['Beverage_category'].isin(popular_categories) & df['Size'].isin(size_order)].groupby(['Beverage_category', 'Size'])['Calories'].mean().unstack(fill_value=0)
size_progression = size_progression.reindex(columns=size_order)

size_progression.plot(kind='bar', stacked=False, figsize=(14, 7), colormap='Greens', alpha=0.8)
plt.xlabel('Beverage Category', fontweight='bold')
plt.ylabel('Average Calories', fontweight='bold')
plt.title('Upselling Strategy: Calorie Progression by Size Across Top Categories\n(Larger gaps indicate stronger upsell opportunities)',
          fontweight='bold', fontsize=14)
plt.legend(title='Size', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/12_size_upgrade_opportunity.png', dpi=300, bbox_inches='tight')
plt.close()


print("=" * 80)
print("Chart generation complete!")
print(f"Generated 12 business insight charts in the 'charts/' directory")
print("=" * 80)
