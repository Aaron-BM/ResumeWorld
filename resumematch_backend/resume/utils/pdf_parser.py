from pypdf import PdfReader

def extract_text_from_pdf(path):
  reader = PdfReader(path)
  text = ''
  for page in reader.pages:
    text += ' ' + (page.extract_text() or '')
  
  return text

def extract_skill_from_parsed_text(text):
  skills = ['python', 'django', 'postgresql', 'html', 'css', 'javascript']
  skills_extracted = set()
  text = text.lower().split()
  for word in text:
    word = word.strip()
    if word in skills:
      skills_extracted.add(word)
  
  return list(skills_extracted)





