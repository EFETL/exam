# 何嘉仁五上第二次段考：挑戰題（自編，難度高於原卷）
HARD = {
 'units': {
  'ph': [
   {'q': '哪一個字的畫線字母組合「發音和其他三個不同」？ (ch)', 'o': ['school', 'lunch', 'chick', 'teacher'], 'a': 0, 'ex': 'school 的 ch 唸 /k/，其他唸 /tʃ/。'},
   {'q': '哪一個字的 th 唸 /ð/（喉嚨會震動）？', 'o': ['this', 'three', 'think', 'thank'], 'a': 0, 'ex': 'this、that、the 的 th 會震動。'},
   {'q': 'photo、phone、dolphin 的 ph 都唸成：', 'o': ['/f/', '/p/', '/h/', '/v/'], 'a': 0, 'ex': 'ph＝/f/。'},
   {'q': '下列哪一組 c 的發音「都是 /s/」？', 'o': ['city, juice, pencil', 'cat, city, cup', 'cool, cake, circle', 'music, cat, cup'], 'a': 0, 'ex': 'c 後面接 e、i、y 唸 /s/。'},
   {'q': '哪一個字要用 tch 而不是 ch？（短母音後面）', 'o': ['ki＿＿＿en（廚房）', 'lun＿＿（午餐）', '＿＿air（椅子）', 'tea＿＿er（老師）'], 'a': 0, 'ex': 'kitchen：短母音 i 後面用 tch。'},
   {'q': '哪一個字的 g 唸 /g/（不是 /dʒ/）？', 'o': ['green', 'giant', 'orange', 'page'], 'a': 0, 'ex': 'g 後面接 r → /g/。'},
   {'q': 'wh 開頭的字，哪一個「不是」問句字？', 'o': ['whale', 'what', 'where', 'who'], 'a': 0, 'ex': 'whale 是鯨魚。'},
  ],
  'subj': [
   {'q': "A: Do you have science today?　B: No, I ＿. I have science ＿ Friday.", 'o': ["don't; on", "don't; in", "am not; on", "doesn't; on"], 'a': 0, 'ex': "No, I don't.；星期前面用 on。"},
   {'q': "A: What subject do you like?　B: ＿", 'o': ["I like art. I can draw a cat.", "I like art. I can sing a song.", "Yes, I like art.", "It's art class."], 'a': 0, 'ex': '畫畫配美勞；唱歌是音樂；What 問句不用 Yes。'},
   {'q': 'Amy 喜歡看地圖、認識臺灣各地，她最喜歡：', 'o': ['social studies', 'math', 'PE', 'music'], 'a': 0, 'ex': '社會課會讀地圖。'},
   {'q': '哪一句「有錯」？', 'o': ['I like chinese and english.', 'I like Chinese and English.', 'Science class is fun.', "I don't like PE."], 'a': 0, 'ex': 'Chinese、English 要大寫。'},
   {'q': "A: ＿ subject do you like, math ＿ science?　B: Math.", 'o': ['Which; or', 'What; and', 'Which; and', 'Who; or'], 'a': 0, 'ex': '兩個選一個 → Which…, A or B?'},
   {'q': '「我喜歡音樂，但我哥哥喜歡體育。」', 'o': ['I like music, but my brother likes PE.', 'I like music, but my brother like PE.', 'I likes music, but my brother likes PE.', 'I like music, and my brother not likes PE.'], 'a': 0, 'ex': 'my brother（他）→ likes。'},
   {'q': 'A: Does Ben like math?　B: ＿', 'o': ["No, he doesn't. He likes art.", "No, he don't. He likes art.", "No, he isn't. He likes art.", "No, I don't."], 'a': 0, 'ex': "Does he…? → No, he doesn't."},
   {'q': '課表：Mon. math／Tue. science／Wed. music。哪一天沒有自然課？', 'o': ['Monday and Wednesday', 'Tuesday', 'Tuesday and Wednesday', 'Every day'], 'a': 0, 'ex': '只有 Tue. 有 science。'},
  ],
  'wea': [
   {'q': "A: How's the weather in Hualien?　B: It's ＿. We can fly a kite.", 'o': ['windy', 'rainy', 'snowy', 'shower'], 'a': 0, 'ex': '放風箏要有風 windy。'},
   {'q': '哪一句的 but 用「錯」了？', 'o': ["It's sunny but hot.", "It's sunny but cold.", "It's rainy but warm.", "It's windy but warm."], 'a': 0, 'ex': '晴天常常熱，sunny 和 hot 同方向 → 用 and。'},
   {'q': "A: Is it cold today?　B: ＿ Let's go swimming!", 'o': ["No, it isn't. It's hot.", "Yes, it is. It's cold.", "No, it isn't. It's cold.", "No, I'm not. It's hot."], 'a': 0, 'ex': '要去游泳 → 天氣熱。'},
   {'q': '25°C、有點風、晴天，最合適的說法是：', 'o': ["It's sunny and warm.", "It's rainy and cold.", "It's cloudy and snowy.", "It's sunny but cold."], 'a': 0, 'ex': '25 度、晴 → sunny and warm。'},
   {'q': '哪一個字和 weather「長得很像」但意思是「水」？', 'o': ['water', 'shower', 'winter', 'wear'], 'a': 0, 'ex': 'water 水。'},
   {'q': '「多麼冷的一天啊！」', 'o': ['What a cold day!', 'What cold a day!', 'How a cold day!', 'What a day cold!'], 'a': 0, 'ex': 'What a＋形容詞＋名詞！'},
   {'q': 'A: How\'s the weather?　B: ＿　（兩句意思都通的是）', 'o': ["It's cloudy. It's cool.", "It's cloudy. I'm cloudy.", "It's Monday. It's cool.", "It's science. It's fun."], 'a': 0, 'ex': '回答天氣與溫度。'},
   {'q': '下雨天出門最需要：', 'o': ['an umbrella', 'a kite', 'a swimsuit', 'sunglasses'], 'a': 0, 'ex': '雨傘 umbrella。'},
  ],
  'gram': [
   {'q': "A: ＿ the weather?　B: It's rainy.　A: ＿ we have PE today?　B: Yes, we do.", 'o': ["How's; Do", "What's; Are", "How's; Are", "Where's; Do"], 'a': 0, 'ex': '問天氣 How\'s；回答 we do → Do 問句。'},
   {'q': '選出「三句都正確」的一組：', 'o': ["Is it hot? / Do you like art? / What a nice day!", "Is it hot? / Are you like art? / What a nice day!", "Does it hot? / Do you like art? / What nice day!", "Is it hot? / Do you likes art? / What a nice day!"], 'a': 0, 'ex': 'Is it＋形容詞；Do you like；What a nice day!'},
   {'q': "A: What day is it today?　B: It's Wednesday.　A: ＿", 'o': ['Do we have music class today?', 'How old are you today?', "Where's Wednesday?", 'What color is Wednesday?'], 'a': 0, 'ex': '知道星期幾後問課表最合理。'},
   {'q': 'Ben ＿ math, but he ＿ like music.', 'o': ["likes; doesn't", "like; don't", "likes; don't", "like; doesn't"], 'a': 0, 'ex': 'Ben（他）→ likes／doesn\'t。'},
   {'q': '哪個問句的回答「不可能」是 Yes, it is.？', 'o': ['Do you have art today?', 'Is it sunny?', 'Is it Monday today?', 'Is science fun?'], 'a': 0, 'ex': 'Do you…? 要用 I do 回答。'},
  ],
 },
 'cloze': [
  {'title': '挑戰克漏字｜A Rainy Friday', 'text': "Today is Friday. It's rainy __1__ cold. We can't play outside. We __2__ PE class today, but we play in the gym. After PE, we have social studies. I like it __3__ I can read maps. My friend Tim doesn't __4__ social studies. He likes math. __5__ a busy day!",
   'qs': [{'q': '__1__', 'o': ['and', 'but', 'or', 'so'], 'a': 0, 'ex': '下雨又冷，同方向 → and。'},
          {'q': '__2__', 'o': ['have', 'has', 'are', 'is'], 'a': 0, 'ex': 'We have PE class.'},
          {'q': '__3__', 'o': ['because', 'but', 'or', 'and so'], 'a': 0, 'ex': '喜歡的原因 → because。'},
          {'q': '__4__', 'o': ['like', 'likes', 'liking', 'to likes'], 'a': 0, 'ex': "doesn't 後面用原形 like。"},
          {'q': '__5__', 'o': ['What', 'How', 'It', 'Is'], 'a': 0, 'ex': 'What a busy day! 感嘆句。'}]}],
 'read': [
  {'title': '挑戰閱讀｜Weekend Plans', 'text': "Mia: How's the weather this weekend, Dad?\nDad: On Saturday, it's sunny and hot. On Sunday, it's windy but warm.\nMia: Great! Let's go swimming on Saturday.\nDad: OK. And on Sunday?\nMia: We can fly my new kite in the park.\nDad: Good idea. But don't forget your science homework. You have science on Monday.",
   'qs': [{'q': 'What can Mia do on Sunday?', 'o': ['Fly a kite.', 'Go swimming.', 'Read maps.', 'Play in the gym.'], 'a': 0, 'ex': 'On Sunday… We can fly my new kite.'},
          {'q': "How's the weather on Saturday?", 'o': ["It's sunny and hot.", "It's windy but warm.", "It's rainy and cold.", "It's cloudy and cool."], 'a': 0, 'ex': 'On Saturday, it\'s sunny and hot.'},
          {'q': 'Why does Mia want to go swimming on Saturday?', 'o': ['Because it is sunny and hot.', 'Because it is windy.', 'Because she has science.', 'Because it is rainy.'], 'a': 0, 'ex': '天氣熱適合游泳。'},
          {'q': '下列哪一個正確？', 'o': ['Mia 星期一有自然課。', 'Mia 星期天要去游泳。', '星期六很涼爽。', '爸爸不讓 Mia 放風箏。'], 'a': 0, 'ex': 'You have science on Monday.'}]}],
 'quick': {
  'subj': [['社會（完整拼出）', 'social studies', ['social study', 'socail studies', 'social studys'], 0, 's'], ['他喜歡自然。', 'He likes science.', ['He like science.', 'He is like science.', 'He likes sience.'], 0, 'g']],
  'wea': [['天氣（完整拼出）', 'weather', ['wether', 'whether', 'weater'], 0, 's'], ['有風但是很溫暖。', "It's windy but warm.", ["It's windy and but warm.", "It windy but warm.", "It's wind but warm."], 0, 'g']],
 },
}
