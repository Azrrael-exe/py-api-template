import datetime
import os

filename = os.getenv("OUTPUT_FILENAME", "hello_world.txt")
# Create the output content
message = "Hello World from Docker + UV!"
timestamp = f"Timestamp: {datetime.datetime.now()}"

# Print to console
print(message)
print(timestamp)

# Save to file
output_content = f"{message}\n{timestamp}\n"
with open(f"data/{filename}", "w") as file:
    file.write(output_content)

print(f"\nOutput has been saved to '{filename}'")

