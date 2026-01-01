import kagglehub

# Download latest version
path = kagglehub.dataset_download("henryshan/starbucks")

print("Path to dataset files:", path)
