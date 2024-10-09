import difflib

def find_prompt_difference(prompt1, prompt2):
    d = difflib.Differ()
    diff = d.compare(prompt1.split(), prompt2.split())
    return ' '.join(diff)

# dxample
prompt1 = "This is a prompt to do some task"
prompt2 = "Prompt number two for some task"
difference = find_prompt_difference(prompt1, prompt2)
print("Prompt Difference:", difference)
