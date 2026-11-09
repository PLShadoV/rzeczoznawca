import fitz,json,warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
from PIL import Image
x=json.load(open('dist/questions.json'));qmap={q['id']:q for q in x['questions']};count=0
for s in x['sessions']:
 if s.get('archive'):continue  # 2018-2021 scans: see data/older/keys_detect.py
 for p in fitz.open('data/'+s['date']+'-key.pdf'):
  pix=p.get_pixmap(matrix=fitz.Matrix(3,3),colorspace=fitz.csGRAY);img=Image.frombytes('L',[pix.width,pix.height],pix.samples)
  for w in p.get_text('words'):
   if not w[4].isdigit() or not 1<=int(w[4])<=90 or not 70<w[0]<335 or not 125<w[1]<710:continue
   q=qmap[s['date']+'-'+w[4]];actual=[]
   for i in range(3):
    left=w[2]+31.5+24*i;top=w[1]-.59
    crop=img.crop((round((left+1.6)*3),round((top+1.6)*3),round((left+6.8)*3),round((top+6.8)*3)))
    density=sum(v<100 for v in crop.getdata())/(crop.width*crop.height)
    if density>.08:actual.append(i)
   assert actual==q['correct'],(q['id'],actual,q['correct'])
   count+=1
assert count==sum(1 for q in x['questions'] if not q['session'] in {s['date'] for s in x['sessions'] if s.get('archive')}),count
print('PASS:',count,'answer sets independently verified against rendered PDF checkboxes.')
