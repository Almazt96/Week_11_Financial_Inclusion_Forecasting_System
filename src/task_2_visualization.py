plt.figure(figsize=(11, 5))
sns.lineplot(x=findex_years, y=findex_access, marker='o', label="Account Ownership (Findex)", color='#2b5c8f')

# Overlay critical intervention milestones
plt.axvline(x=2021.37, color='red', linestyle='--', alpha=0.7, label="Telebirr Launch (May 2021)") [cite: 190]
plt.axvline(x=2023.66, color='green', linestyle='--', alpha=0.7, label="M-Pesa Launch (Aug 2023)") [cite: 191]

plt.title("Ethiopia: Account Ownership vs. Market Intervention Events")
plt.xlabel("Year")
plt.ylabel("Inclusion Rate")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.3)
plt.show()