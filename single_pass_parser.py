example = """<span class="spoiler" title="x">Crovax</span> becomes one of these in the final chapter."""

sentences = list()
i = 0
is_spoiler = False
start = 0
while i < len(example):
    if example[i] == "<":
        if example[i + 1] == "/":
            # ending tag
            i = i + len("""</span>""")
            is_spoiler = False
        else:
            # opening tag
            i = i + len("""<span class="spoiler" title="x">""")
            is_spoiler = True
        continue

    i += 1
