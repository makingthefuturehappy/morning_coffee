import text_processor

x = "Dr. Joe Biden announced a new plan on student loan forgiveness. The application for loan forgiveness will become available in early October. Borrowers are advised to apply by Nov.15 in order to receive relief before the payment pause expires on Dec. 31. Roughly 7 million borrowers will qualify for forgiveness under the plan."
print(x)
x = text_processor.clean_text(x)
print(x)
