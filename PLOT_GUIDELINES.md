# Plot Guidelines - Ensuring Story Adherence

Guide for writing effective plots that the AI will follow faithfully.

## 📏 Plot Length Recommendations

### Optimal Lengths

| Length | Characters | Words | Adherence | Use Case |
|--------|-----------|-------|-----------|----------|
| **Minimal** | 50-200 | 10-40 | Low | Quick tests only |
| **Good** | 200-500 | 40-100 | Medium | Simple stories |
| **Recommended** | 500-1500 | 100-300 | High | Most stories |
| **Detailed** | 1500-2500 | 300-500 | Very High | Complex plots |
| **Maximum** | 2500-4000 | 500-800 | High* | Epic stories |

*May need special handling for very long plots

### Technical Limits

- **Model Context Window**: 
  - Mistral-7B: ~8000 tokens (~6000 words)
  - TinyLlama: ~2000 tokens (~1500 words)
- **Recommended Plot**: 500-2000 characters (safe for all models)
- **Maximum Practical**: 4000 characters

---

## ✅ How to Write Plots for Maximum Adherence

### 1. Use Structured Format

**Template:**
```
TITLE: [Story Title]

CHARACTERS:
- [Name]: [Description, personality, key traits]
- [Name]: [Description, personality, key traits]

SETTING:
[Where and when the story takes place]

PLOT:
[Main story arc - beginning, middle, end]

CONFLICT:
[The main challenge or problem]

RESOLUTION:
[How the conflict is resolved]

KEY SCENES:
1. [Important scene to include]
2. [Important scene to include]
3. [Important scene to include]

THEMES:
[Core messages and lessons]

TONE:
[Humorous, serious, adventurous, etc.]
```

### 2. Example: Minimal Plot (Low Adherence)

```python
story_idea = {
    'plot': 'A kid makes friends at school',
    'themes': ['friendship'],
    'length': 'short'
}
```

**Issues:**
- Too vague
- No character details
- No specific conflict
- Model will improvise heavily

### 3. Example: Good Plot (Medium Adherence)

```python
story_idea = {
    'plot': '''
    A shy 9-year-old named Emma moves to a new school. She's nervous about 
    making friends. On her first day, she discovers a secret garden behind 
    the library where she meets other kids who also feel like outsiders. 
    Together they form a friendship club.
    ''',
    'themes': ['friendship', 'courage', 'belonging'],
    'length': 'short'
}
```

**Better because:**
- Named character
- Clear setting
- Specific conflict (new school)
- Resolution hint (friendship club)

### 4. Example: Excellent Plot (High Adherence)

```python
story_idea = {
    'plot': '''
    CHARACTERS:
    - Leo Martinez: A plump, witty 9-year-old with curly brown hair and 
      expressive eyes. New to Oakwood Elementary. Uses humor to cope with 
      nervousness. Loves comic books and drawing.
    - Maya Chen: A quiet 8-year-old with long black hair and glasses. 
      Sits alone on the Friendship Bench. Excellent artist but shy about 
      sharing her work.
    - Jake and his friends: The "cool kids" who sometimes tease others.
    
    SETTING:
    Oakwood Elementary School, first week of 4th grade, September. 
    The school has a special "Friendship Bench" where kids sit when 
    they want someone to play with.
    
    PLOT:
    Leo is terrified on his first day at a new school. During recess, 
    he notices Maya sitting alone on the Friendship Bench, looking sad. 
    Despite his own fears, Leo decides to approach her, using a joke 
    about the bench being "the coolest seat in school."
    
    Maya is surprised but laughs. They discover they both love drawing 
    and comic books. Leo shows Maya his superhero sketches, and Maya 
    shares her manga-style drawings.
    
    CONFLICT:
    Jake and his friends make fun of Leo's weight during lunch. Leo 
    tries to laugh it off, but he's hurt. Maya, despite being shy, 
    stands up for Leo, telling Jake that real friends don't make fun 
    of each other. Her courage surprises everyone, including herself.
    
    RESOLUTION:
    Inspired by Maya's bravery, Leo suggests they start a comic book 
    club that meets at the Friendship Bench. By Friday, five other 
    kids have joined. The Friendship Bench becomes the headquarters 
    for their club. Leo realizes that being kind and brave matters 
    more than being popular.
    
    KEY SCENES TO INCLUDE:
    1. Leo's nervous first morning, meeting the principal
    2. Leo approaching Maya at the Friendship Bench with his joke
    3. Leo and Maya discovering their shared love of comics
    4. The lunch incident with Jake's teasing
    5. Maya standing up for Leo
    6. The first comic book club meeting with all the new friends
    
    THEMES:
    - Kindness can overcome fear
    - True friendship means standing up for each other
    - Being different is okay
    - Humor can help in difficult situations
    - Small acts of courage can inspire others
    
    TONE:
    Warm, humorous, uplifting. Show Leo's wit through dialogue. 
    Include moments of vulnerability but always end scenes on a 
    hopeful note.
    ''',
    'themes': ['friendship', 'kindness', 'courage', 'humor'],
    'target_age': '8-12',
    'length': 'short',
    'art_style': 'children_book'
}
```

**Why this works:**
- ✅ Detailed character descriptions
- ✅ Clear setting with specific details
- ✅ Well-defined plot arc
- ✅ Specific conflict and resolution
- ✅ Key scenes listed
- ✅ Themes explicitly stated
- ✅ Tone guidance
- ✅ ~1800 characters (optimal length)

---

## 🎯 Tips for Maximum Adherence

### 1. Be Specific About Characters

**Bad:**
```
A kid who likes animals
```

**Good:**
```
Emma Rodriguez, age 10, with freckles and red braids. She's passionate 
about wildlife conservation and dreams of being a veterinarian. She's 
brave with animals but shy around people.
```

### 2. Define Clear Conflicts

**Bad:**
```
They face a problem
```

**Good:**
```
The school garden is going to be demolished to build a parking lot. 
Emma has only one week to convince the principal to save it by showing 
how many students use it for their science projects.
```

### 3. Specify Key Scenes

```python
KEY SCENES TO INCLUDE:
1. Emma discovering the demolition notice
2. Emma presenting her case to the principal
3. The student rally to save the garden
4. The final decision and celebration
```

### 4. Use Dialogue Examples

```
Include dialogue like:
- Leo's opening joke: "Is this the VIP section? Because this bench 
  looks way too fancy for regular kids."
- Maya's brave moment: "That's not funny, Jake. Leo is my friend, 
  and friends don't treat each other like that."
```

### 5. Specify Emotional Beats

```
EMOTIONAL ARC:
- Chapter 1: Leo feels anxious and alone
- Chapter 2: Leo feels hopeful after meeting Maya
- Chapter 3: Leo feels hurt by teasing but inspired by Maya's courage
- Ending: Leo feels confident and happy with his new friends
```

---

## 🔧 Technical Implementation

### For Python API Users

```python
from orchestrator.coordinator import StoryOrchestrator

# Load your detailed plot from a file
with open('my_detailed_plot.txt', 'r') as f:
    detailed_plot = f.read()

story_idea = {
    'plot': detailed_plot,  # Can be 500-2500 characters
    'target_age': '8-12',
    'themes': ['friendship', 'courage', 'kindness'],
    'length': 'short',
    'art_style': 'children_book'
}

orchestrator = StoryOrchestrator()
result = orchestrator.create_story(story_idea)
```

### For Very Long Plots (2500+ characters)

If your plot exceeds 2500 characters, consider:

**Option 1: Break into sections**
```python
plot = f"""
{character_descriptions}

{setting_details}

{plot_outline}

{key_scenes}

{themes_and_tone}
"""
```

**Option 2: Use a separate character file**
```python
story_idea = {
    'plot': main_plot,  # Keep under 2000 chars
    'character_descriptions': character_file,  # Additional details
    'themes': themes_list,
    'length': 'medium'
}
```

---

## 📊 Testing Plot Adherence

### Quick Test

Create a test story with very specific requirements:

```python
test_plot = """
MUST INCLUDE:
- A character named "Sparkle" who is a purple dragon
- A magical library with floating books
- Exactly 3 wishes that go wrong
- A friendship between Sparkle and a bookworm named Tim
- Ending with Sparkle learning to read

DO NOT INCLUDE:
- Any violence or scary scenes
- Other dragons
- Parents or adults as main characters
"""

# Generate and check if requirements are met
```

### Verification Checklist

After generation, check:
- [ ] All named characters appear
- [ ] Setting matches description
- [ ] Key scenes are included
- [ ] Conflict and resolution match
- [ ] Themes are evident
- [ ] Tone is appropriate

---

## 🎨 Plot Templates

### Template 1: Adventure Story

```
CHARACTERS:
- [Hero name, age, key trait]
- [Companion name, age, key trait]
- [Antagonist/obstacle]

SETTING:
[Specific location and time]

QUEST:
[What they're trying to achieve]

OBSTACLES:
1. [First challenge]
2. [Second challenge]
3. [Final challenge]

RESOLUTION:
[How they succeed and what they learn]
```

### Template 2: Friendship Story

```
CHARACTERS:
- [Character 1: personality, interests]
- [Character 2: personality, interests]

INITIAL SITUATION:
[How they meet or why they're apart]

CONFLICT:
[What threatens or tests their friendship]

TURNING POINT:
[Moment when things change]

RESOLUTION:
[How friendship is strengthened]
```

### Template 3: Problem-Solving Story

```
PROTAGONIST:
[Name, age, special skill or interest]

PROBLEM:
[Clear, specific problem to solve]

ATTEMPTS:
1. [First attempt and why it fails]
2. [Second attempt and why it fails]
3. [Creative solution that works]

LESSON:
[What the character learns]
```

---

## 💡 Pro Tips

### 1. Front-Load Important Details

Put the most important information at the beginning of your plot:

```
MOST IMPORTANT: This story must show how kindness is more powerful 
than popularity. The main character, Leo, should use humor throughout.

[Rest of plot details...]
```

### 2. Use Repetition for Key Points

```
Leo is witty and uses humor to cope. Throughout the story, Leo should 
make jokes and use his sense of humor to handle difficult situations. 
His humor is his superpower.
```

### 3. Specify What NOT to Include

```
DO NOT INCLUDE:
- Any violence or fighting
- Romantic relationships
- Adult characters solving the problem
- Magic or supernatural elements
```

### 4. Give Style Examples

```
WRITING STYLE:
Use short, punchy sentences for action. Include lots of dialogue. 
Example: "Leo grinned. 'Want to see my superhero drawings?' Maya 
nodded, her eyes lighting up."
```

---

## 📈 Plot Length Impact on Quality

| Plot Length | Generation Time | Adherence | Story Quality | Recommendation |
|-------------|----------------|-----------|---------------|----------------|
| 50-200 chars | Fastest | 40-60% | Variable | Testing only |
| 200-500 chars | Fast | 60-75% | Good | Simple stories |
| 500-1500 chars | Normal | 80-90% | Excellent | **Recommended** |
| 1500-2500 chars | Normal | 90-95% | Excellent | Complex plots |
| 2500+ chars | Slower | 85-90%* | Excellent | Use with care |

*May lose some details due to context limits

---

## 🎯 Summary

**For Best Results:**

1. **Length**: 500-2000 characters (100-400 words)
2. **Structure**: Use clear sections (Characters, Setting, Plot, etc.)
3. **Specificity**: Name characters, describe settings, define conflicts
4. **Key Scenes**: List 3-6 must-include scenes
5. **Themes**: Explicitly state themes and tone
6. **Examples**: Include dialogue or scene examples
7. **Constraints**: Specify what NOT to include

**Example Perfect Plot Length:**
```python
len(excellent_plot_example)  # ~1800 characters
# This is the sweet spot for maximum adherence
```

---

Your plot can be as detailed as you want (up to ~4000 characters), but **500-2000 characters with clear structure gives the best adherence**! 🎯
