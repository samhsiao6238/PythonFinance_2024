import google.generativeai as genai

print('Available base models:', [m.name for m in genai.list_models()])