import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Schema mapping events to impacts
association_data = {
    'Event': ['Telebirr Launch', 'M-Pesa Entry', 'National Payment Strategy', 'Fayda ID Rollout'],
    'ACC_OWNERSHIP': [0.08, 0.04, 0.05, 0.12], # Estimated Max Coefficients
    'USG_DIGITAL_PAYMENT': [0.15, 0.08, 0.10, 0.05],
    'ACC_MM_ACCOUNT': [0.22, 0.12, 0.05, 0.08]
}

df_matrix = pd.DataFrame(association_data).set_index('Event')

# Display heatmap
plt.figure(figsize=(8, 4))
sns.heatmap(df_matrix, annot=True, cmap="Purples", fmt=".2f", cbar=True)
plt.title("Event-Indicator Impact Association Matrix (Magnitude)")
plt.tight_layout()
plt.show()