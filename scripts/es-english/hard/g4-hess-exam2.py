# 何嘉仁四上第二次段考：挑戰題（自編，難度高於原卷）
HARD = {
 'units': {
  'ph': [
   {'q': '哪一個字「不屬於」同一個字族？ cat、hat、mat、＿', 'o': ['cut', 'bat', 'rat', 'sat'], 'a': 0, 'ex': 'cut 是 -ut 家族，其他是 -at。'},
   {'q': '哪一組三個字的「母音」都一樣？', 'o': ['map, bag, cat', 'map, mop, cup', 'pen, pin, pan', 'sun, son, sat'], 'a': 0, 'ex': 'map、bag、cat 都是短 a。'},
   {'q': '哪一個字只換掉「第一個字母」就能從 mop 變成？', 'o': ['top', 'map', 'mob', 'pot'], 'a': 0, 'ex': 'mop → top，只換 m→t。'},
   {'q': 'c_t 空格填不同母音可以變出幾個真的字？（cat、cot、cut…）', 'o': ['3 個（a、o、u）', '1 個', '2 個', '5 個'], 'a': 0, 'ex': 'cat 貓、cot 小床、cut 切；cit、cet 不是常用字。'},
   {'q': '哪兩個字「開頭音」一樣，「母音」也一樣？', 'o': ['bag — bat', 'bag — big', 'bag — tag', 'bag — bed'], 'a': 0, 'ex': 'bag、bat：b＋短 a。'},
   {'q': '小美把 fan 唸成 van，她搞錯了哪兩個音？', 'o': ['f 和 v', 'a 和 e', 'n 和 m', 'f 和 p'], 'a': 0, 'ex': 'f 不震動、v 會震動。'},
  ],
  'room': [
   {'q': "A: Where's Grandpa?　B: ＿ in the ＿. He's cooking.", 'o': ["He's; kitchen", "She's; kitchen", "He's; bedroom", "He; kitchen"], 'a': 0, 'ex': '爺爺是男生 → He\'s；煮飯在廚房。'},
   {'q': 'A: Where are you, Mom?　B: ＿ in the bathroom.', 'o': ["I'm", "She's", "You're", "Mom's"], 'a': 0, 'ex': '媽媽回答自己 → I\'m。'},
   {'q': '下列哪一組對話「不」合理？', 'o': ["A: Where's your dad? B: He's my dad.", "A: Where's your dad? B: He's in the living room.", "A: Who's she? B: She's my sister.", "A: Where are you? B: I'm in the kitchen."], 'a': 0, 'ex': '問「在哪裡」卻回答「他是我爸爸」。'},
   {'q': "A: I can't find my sister.　B: ＿", 'o': ["She's in the dining room. She's eating.", "He's in the dining room.", "She's in the dining room. She's sleeping.", "I'm your sister."], 'a': 0, 'ex': '姊妹 → She\'s；在餐廳應該在吃飯。'},
   {'q': '哪一句寫法完全正確？', 'o': ["Where's your brother?", "Where your brother?", "Where's your brother.", "where's your brother?"], 'a': 0, 'ex': 'Where\'s＝Where is；問句用問號；句首大寫。'},
   {'q': '「我的祖父母在客廳。」', 'o': ['My grandparents are in the living room.', 'My grandparents is in the living room.', "My grandparents in the living room.", "My grandparents are in living room."], 'a': 0, 'ex': '兩個人 → are；in the living room 要有 the。'},
   {'q': 'A: Where ＿ Tom and Ken?　B: They\'re in the bedroom.', 'o': ['are', 'is', 'am', "'s"], 'a': 0, 'ex': '兩個人 → are。'},
   {'q': '在 bathroom 最可能做什麼？', 'o': ['刷牙洗澡', '看電視', '煮晚餐', '睡午覺'], 'a': 0, 'ex': 'bathroom 浴室。'},
   {'q': '重組：( your / Where\'s / mom / ? ) → 回答：( She\'s / kitchen / the / in / . )', 'o': ["Where's your mom? / She's in the kitchen.", "Your mom where's? / She's the in kitchen.", "Where's mom your? / In the kitchen she's.", "Where's your mom. / She's in kitchen the."], 'a': 0, 'ex': '問：Where\'s your mom?　答：She\'s in the kitchen.'},
  ],
  'pet': [
   {'q': 'A: Do you have a dog?　B: ＿ I have a cat.', 'o': ["No, I don't.", 'Yes, I do.', "No, I'm not.", 'Yes, I have.'], 'a': 0, 'ex': '後面說有貓 → 沒有狗：No, I don\'t.'},
   {'q': '哪一句「有錯」？', 'o': ['I have fish.', 'I have a fish.', 'Do you have a turtle?', "No, I don't."], 'a': 0, 'ex': '一隻魚要說 a fish（段考常扣分）。'},
   {'q': 'A: ＿　B: Yes, I do. It\'s a rabbit.', 'o': ['Do you have a pet?', 'Are you a rabbit?', "What's your pet's name?", 'Where is the rabbit?'], 'a': 0, 'ex': '用 Yes, I do. 回答 → Do 問句。'},
   {'q': 'A: Are you a turtle?　B: ＿', 'o': ["No, I'm not. I'm a boy.", "No, I don't.", 'Yes, I do.', "No, it isn't."], 'a': 0, 'ex': 'Are you…? → I\'m／I\'m not，跟 Do you…? 不一樣。'},
   {'q': '下列哪一個「不是」寵物？', 'o': ['kitchen', 'rabbit', 'turtle', 'bird'], 'a': 0, 'ex': 'kitchen 是廚房。'},
   {'q': '「我沒有養鳥，但我有一隻烏龜。」', 'o': ["I don't have a bird, but I have a turtle.", "I not have a bird, but I have a turtle.", "I'm not have a bird, but I have a turtle.", "I don't have bird, but I have turtle."], 'a': 0, 'ex': "don't have；要有 a。"},
   {'q': 'A: Do you have a fish?　B: Yes, I ＿. It\'s in the ＿ room.', 'o': ['do; living', 'am; living', 'do; bath', 'have; living'], 'a': 0, 'ex': 'Yes, I do.；living room 客廳。'},
   {'q': '哪一個動物「不會」飛也「不會」游泳？', 'o': ['rabbit', 'bird', 'fish', 'turtle'], 'a': 0, 'ex': '兔子在地上跑跳。'},
  ],
  'gram': [
   {'q': "A: ＿ he?　B: He's my uncle.　A: ＿ he?　B: He's in the kitchen.", 'o': ["Who's; Where's", "Where's; Who's", "What's; Where's", "Who's; What's"], 'a': 0, 'ex': '問誰 Who\'s，問在哪 Where\'s。'},
   {'q': '下列哪一個回答「同時」適合 Do you have a cat? 和 Do you have a dog?', 'o': ["No, I don't.", "No, I'm not.", "It's a cat.", "She's my cat."], 'a': 0, 'ex': 'Do 問句都用 I do／I don\'t 回答。'},
   {'q': 'A: Is she a doctor?　B: ＿', 'o': ["No, she isn't. She's a teacher.", "No, she don't. She's a teacher.", "No, he isn't. She's a teacher.", "No, I'm not."], 'a': 0, 'ex': 'Is she…? → No, she isn\'t.'},
   {'q': '選出 be 動詞全部正確的一句：', 'o': ["I'm in the kitchen. Mom is in the bedroom. They are happy.", "I is in the kitchen. Mom are in the bedroom.", "I am in the kitchen. Mom am in the bedroom.", "I'm in the kitchen. Mom are in the bedroom."], 'a': 0, 'ex': 'I am、Mom is、They are。'},
   {'q': 'A: Where are your dogs?　B: ＿', 'o': ["They're in the living room.", "It's in the living room.", "He's in the living room.", "They're is in the living room."], 'a': 0, 'ex': 'dogs 複數 → They\'re。'},
   {'q': "A: Nice to meet you. I'm Ben.　B: ＿", 'o': ["Nice to meet you, too. I'm Amy.", "Nice to meet you. I'm fine.", "You're welcome. I'm Amy.", 'Yes, I do.'], 'a': 0, 'ex': '回 Nice to meet you, too. 再自我介紹。'},
  ],
 },
 'cloze': [
  {'title': '挑戰克漏字｜Where Is Everyone?', 'text': "It's Sunday. Where is everyone? My dad __1__ in the kitchen. He is cooking lunch. My mom and my sister __2__ in the living room. They are reading. Where's my grandma? __3__ in the garden with our dog, Lucky. Do I have a pet, too? Yes, I __4__. I have two fish. They're in __5__ bedroom.",
   'qs': [{'q': '__1__', 'o': ['is', 'are', 'am', 'do'], 'a': 0, 'ex': 'My dad 一個人 → is。'},
          {'q': '__2__', 'o': ['are', 'is', 'am', 'do'], 'a': 0, 'ex': '媽媽和姊姊兩個人 → are。'},
          {'q': '__3__', 'o': ["She's", "He's", "It's", "They're"], 'a': 0, 'ex': 'grandma 女生 → She\'s。'},
          {'q': '__4__', 'o': ['do', 'am', 'have', 'is'], 'a': 0, 'ex': 'Do I have…? → Yes, I do.'},
          {'q': '__5__', 'o': ['my', 'I', 'me', "I'm"], 'a': 0, 'ex': '「我的」臥室 → my bedroom。'}]}],
 'read': [
  {'title': '挑戰閱讀｜Hide and Seek', 'text': "Kevin and his family are playing hide-and-seek.\nKevin: Where's Dad? He isn't in the bathroom.\nMom: Look in the kitchen!\nKevin: No, he isn't in the kitchen. But Dad's cat, Mimi, is in the kitchen.\nGrandma: I can see a big foot. It's under the bed!\nKevin: Ha! Dad is in my bedroom!",
   'qs': [{'q': "Where's Kevin's dad?", 'o': ['In the bedroom.', 'In the kitchen.', 'In the bathroom.', 'In the living room.'], 'a': 0, 'ex': 'Dad is in my bedroom!'},
          {'q': 'Who has a cat?', 'o': ["Kevin's dad.", 'Kevin.', 'Grandma.', 'Mom.'], 'a': 0, 'ex': "Dad's cat, Mimi."},
          {'q': 'Where is Mimi?', 'o': ['In the kitchen.', 'Under the bed.', 'In the bathroom.', "In Kevin's bedroom."], 'a': 0, 'ex': 'Mimi is in the kitchen.'},
          {'q': '奶奶怎麼知道爸爸在哪裡？', 'o': ['她看到床底下有一隻大腳', '她聽到爸爸在唱歌', '貓咪告訴她', '爸爸在廚房煮飯'], 'a': 0, 'ex': 'I can see a big foot. It\'s under the bed!'}]}],
 'quick': {
  'room': [['餐廳（完整拼出）', 'dining room', ['dinning room', 'dining rom', 'dineing room'], 0, 's'], ['他們在客廳。', "They're in the living room.", ["They in the living room.", "They're in living room.", "There in the living room."], 0, 'g']],
  'pet': [['昆蟲（完整拼出）', 'insect', ['insact', 'inseck', 'insert'], 0, 's'], ['我沒有養狗。', "I don't have a dog.", ["I not have a dog.", "I'm not have a dog.", "I don't have dog."], 0, 'g']],
 },
}
