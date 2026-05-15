import asyncio
import json

from sqlalchemy import select

from app.db.models.course_lessons import CourseLesson
from app.db.session import async_session_maker as SessionLocal


# HSK4 Standard Course 4 (B), lessons 12-20.
# Chinese vocabulary and dialogues are transcribed from the textbook. Localized meanings
# are bot UI translations, following the same shape as the HSK2 seed files.
LESSON_DATA = {
    12: {
        "title": "用心发现世界",
        "vocab": [
            ("规定", "guīdìng", "n. rule, regulation"),
            ("死", "sǐ", "adj. rigid, inflexible"),
            ("可惜", "kěxī", "adj. pitiful, regretful"),
            ("全部", "quánbù", "n. all, whole"),
            ("也许", "yěxǔ", "adv. maybe, perhaps"),
            ("商量", "shāngliang", "v. to discuss, to consult"),
            ("并且", "bìngqiě", "conj. and"),
            ("盐", "yán", "n. salt"),
            ("勺（子）", "sháo(zi)", "n. spoon"),
            ("保护", "bǎohù", "v. to protect"),
            ("作用", "zuòyòng", "n. function"),
            ("无法", "wúfǎ", "v. cannot, to be unable"),
            ("节", "jié", "m. section, length"),
            ("详细", "xiángxì", "adj. detailed"),
            ("解释", "jiěshì", "v. to explain"),
            ("对于", "duìyú", "prep. for, to, with regard to"),
            ("叶子", "yèzi", "n. leaf"),
            ("教育", "jiàoyù", "v. to educate"),
        ],
        "dialogues": [
            (
                "课文 1",
                "王经理做生意遇到了困难",
                [
                    ("王经理", "听说这次生意你到现在还没谈成。"),
                    ("马经理", "按我以前的经验，早应该谈成了，这次我也不知道哪儿出了问题。"),
                    ("王经理", "有句话叫“规定和经验是死的，人是活的”。当“规定”和“经验”不能解决问题时，建议你改变一下自己的态度和想法。"),
                    ("马经理", "很多时候，我都习惯根据过去的经验做事，可惜，经验不是全部都是对的。"),
                    ("王经理", "遇到不能解决的问题时，我们应该试着走走以前从来没走过的路，也许这样就能找到解决问题的方法了。"),
                    ("马经理", "好，我再跟同事商量商量，希望能及时发现问题，并且准确地找到解决问题的方法。"),
                ],
            ),
            (
                "课文 2",
                "高老师告诉女儿洗衣服的方法",
                [
                    ("女儿", "妈，您看我刚买的裤子，洗完以后颜色怎么变得这么难看呢？"),
                    ("高老师", "看来是掉颜色了，你洗的时候在水里加点儿盐就不会这样了。"),
                    ("女儿", "放盐？！盐不是用来做饭的吗？难道它还能让衣服不掉颜色？"),
                    ("高老师", "当然。有些衣服第一次洗的时候会掉颜色，其实，有很多方法可以解决这个问题。在水里加勺盐再洗是最简单的方法。用盐水来洗新衣服，这样穿得再久、洗的次数再多，衣服也不容易掉颜色。"),
                    ("女儿", "我第一次听说盐有保护衣服颜色的作用，生活中还真有不少课本上无法学到的知识。"),
                    ("高老师", "实际上，很多问题的答案都可以从生活中找到。但这需要你用眼睛去发现，用心去总结。"),
                ],
            ),
            (
                "课文 3",
                "高老师学习王教授的教育方法",
                [
                    ("高老师", "王教授，今天听完您的这节课，我终于明白为什么您的课那么受学生欢迎了。"),
                    ("王教授", "谢谢！您能详细谈谈对我的课的看法吗？"),
                    ("高老师", "我发现您对学生特别了解，而且总是能用最简单的方法把复杂的问题解释清楚，让每个学生都能听懂，这一点真是值得我们好好儿学习。"),
                    ("王教授", "哪里哪里，这只是因为我对每个学生的能力水平比较了解。"),
                    ("高老师", "那您认为对于老师来说，什么是最难做到的？"),
                    ("王教授", "世界上没有完全相同的叶子，同样地，世界上也没有完全一样的人。所以，在教育学生时，要根据学生的特点选择不同的方法，我想这应该是最不容易做到的。"),
                ],
            ),
        ],
    },
    13: {
        "title": "喝着茶看京剧",
        "vocab": [
            ("京剧", "jīngjù", "n. Beijing opera"),
            ("演员", "yǎnyuán", "n. actor/actress"),
            ("观众", "guānzhòng", "n. audience"),
            ("厚", "hòu", "adj. deep, profound"),
            ("演出", "yǎnchū", "v. to perform, to put on a show"),
            ("大概", "dàgài", "adv. roughly, approximately"),
            ("来自", "láizì", "v. to be from"),
            ("遍", "biàn", "m. denoting an action from beginning to end"),
            ("偶尔", "ǒu'ěr", "adv. occasionally, once in a while"),
            ("吃惊", "chījīng", "v. to be surprised, to be shocked"),
            ("基础", "jīchǔ", "n. basis, foundation"),
            ("表演", "biǎoyǎn", "v. to act, to perform"),
        ],
        "dialogues": [
            (
                "课文 1",
                "小雨和小夏在聊小夏的爷爷表演京剧的情况",
                [
                    ("小雨", "小夏，你爷爷京剧唱得真专业，我还以为他是京剧演员呢。"),
                    ("小夏", "对啊，他本来就是京剧演员，年轻时在我们那儿很有名，深受观众们的喜爱。"),
                    ("小雨", "你爷爷一定对京剧有着很深厚的感情。"),
                    ("小夏", "是呀，他8岁就开始上台演出，到现在大概唱了60多年了，他对这门艺术的喜爱从来没有改变过。"),
                    ("小雨", "这么说你喜欢听京剧也是受了你爷爷的影响？"),
                    ("小夏", "我小时候经常去看他的演出。平时他还给我讲很多京剧里的历史故事，让我学到了很多知识。"),
                ],
            ),
            (
                "课文 2",
                "小雨和马克在聊京剧",
                [
                    ("小雨", "真没想到你一个来自美国的外国留学生，能把京剧唱得这么好。"),
                    ("马克", "我常常跟着电视学唱京剧，然后一遍一遍地练习，偶尔跟中国人一起唱上几句。"),
                    ("小雨", "难道你从来没有接受过京剧方面的专门教育吗？"),
                    ("马克", "别吃惊，因为我以前学习过音乐，有一些音乐基础，又对京剧这种表演艺术非常感兴趣，所以能比较容易地学会它的唱法。"),
                    ("小雨", "你真厉害！竟然连很多中国人都听不懂的京剧也能学会。我还是比较喜欢听流行音乐。"),
                    ("马克", "那是你不了解京剧的唱法。在音乐方面，京剧给了我很多新的想法。我还把京剧的一些特点增加到了自己的音乐中，达到了很好的效果。"),
                ],
            ),
        ],
    },
    14: {
        "title": "保护地球母亲",
        "vocab": [
            ("出差", "chūchāi", "v. to go on a business trip"),
            ("毛巾", "máojīn", "n. towel"),
            ("牙膏", "yágāo", "n. toothpaste"),
            ("重", "zhòng", "adj. heavy, weighty"),
            ("行", "xíng", "v. to be OK, to be all right"),
            ("省", "shěng", "v. to save, to economize"),
            ("污染", "wūrǎn", "v. to pollute"),
            ("卫生间", "wèishēngjiān", "n. restroom, bathroom"),
            ("脏", "zāng", "adj. dirty"),
            ("抱歉", "bàoqiàn", "v. to be sorry"),
            ("空", "kōng", "adj. empty"),
            ("盒子", "hézi", "n. box, case"),
            ("扔", "rēng", "v. to throw away"),
            ("以", "yǐ", "prep. via, by means of"),
            ("速度", "sùdù", "n. speed"),
            ("地球", "dìqiú", "n. earth, globe"),
            ("既然", "jìrán", "conj. since, as, now that"),
            ("停", "tíng", "v. to stop, to cease"),
            ("得意", "déyì", "adj. complacent, gloating"),
            ("目的", "mùdì", "n. aim, purpose"),
            ("暖", "nuǎn", "adj. warm"),
        ],
        "dialogues": [
            (
                "课文 1",
                "李进要出差，王静和李进在聊天儿",
                [
                    ("王静", "这是明天你出差要带的毛巾、牙膏和牙刷，把它们放到箱子里吧。"),
                    ("李进", "不用拿这些，宾馆都会免费提供的。再说，箱子已经够重的了！"),
                    ("王静", "我当然知道宾馆里有。你不是一直说要保护环境吗？现在就从身边的小事做起吧。"),
                    ("李进", "行，没问题。我明天上午10点的飞机，你能开车把我送到机场吗？"),
                    ("王静", "那个时间路上堵车多严重啊！你还是坐地铁去机场吧。这样不仅省油钱，而且还不会污染空气。"),
                    ("李进", "好，那就听你的。"),
                ],
            ),
            (
                "课文 2",
                "经理和服务员在谈工作",
                [
                    ("经理", "小王，卫生间怎么那么脏啊？这会给客人留下不好的印象，快去打扫一下。"),
                    ("服务员", "经理，实在抱歉。今天店里太忙了，我还没来得及打扫。"),
                    ("经理", "那张桌子下面还有一些空饮料瓶子和纸盒子。"),
                    ("服务员", "好的，我马上就去把它们扔掉。"),
                    ("经理", "以后你一定得注意这个问题，不管客人多不多，生意多忙，我们都要保证餐厅干净卫生。"),
                    ("服务员", "经理您放心，我一定以最快的速度完成。不过咱们真的应该再多招聘几个服务员了。"),
                ],
            ),
            (
                "课文 3",
                "孙月和王静在聊关于环保的事情",
                [
                    ("孙月", "早上听新闻说明天有一个叫“地球一小时”的活动，你对这个活动了解吗？"),
                    ("王静", "这个活动年年都有，最早是从2007年开始的。明天晚上很多人都会关灯一小时，支持这个活动。你没看到门口的通知吗？我们公司也参加。"),
                    ("孙月", "真的吗？太好了！既然明天晚上公司会关灯停电，那么我们肯定不用加班了。"),
                    ("王静", "看你得意的样子！还以为你高兴是为了支持环保，原来是因为不用加班啊！"),
                    ("孙月", "环境保护我当然也支持了！对了，为什么会有这么一个活动啊？"),
                    ("王静", "其实目的挺简单的，就是提醒人们节约用电，希望引起人们对气候变暖问题的关注。"),
                ],
            ),
        ],
    },
    15: {
        "title": "教育孩子的艺术",
        "vocab": [
            ("弹钢琴", "tán gāngqín", "to play the piano"),
            ("棒", "bàng", "adj. excellent, amazing"),
            ("孙子", "sūnzi", "n. grandson"),
            ("寒假", "hánjià", "n. winter vacation"),
            ("父亲", "fùqin", "n. father"),
            ("闹钟", "nàozhōng", "n. alarm clock"),
            ("响", "xiǎng", "v. to sound, to ring"),
            ("醒", "xǐng", "v. to wake up, to be awake"),
            ("赶", "gǎn", "v. to rush for, to hurry"),
            ("厕所", "cèsuǒ", "n. lavatory, toilet"),
            ("批评", "pīpíng", "v. to criticize"),
            ("弄", "nòng", "v. to do, to make"),
            ("管理", "guǎnlǐ", "v. to manage, to administer"),
        ],
        "dialogues": [
            (
                "课文 1",
                "李老师建议王静让孩子养成好习惯",
                [
                    ("王静", "那个一边弹钢琴一边唱歌的男孩子是谁？表演得真棒！"),
                    ("李老师", "是我孙子。去年寒假前的新年晚会他也表演过一次。"),
                    ("王静", "我想起来了，这孩子又聪明又可爱，你们教育得真好！"),
                    ("李老师", "是他父母教育得好。父母是孩子最重要的老师。他父母不仅教他知识，而且还花了很长时间帮助他养成了非常好的习惯，现在他每天都自己练习弹钢琴。"),
                    ("王静", "让孩子养成一个好习惯实在太重要了，看来我得向他父母好好儿学习。"),
                    ("李老师", "对。如果希望有一个优秀的孩子，你就要先成为一位优秀的父亲或者母亲。"),
                ],
            ),
            (
                "课文 2",
                "王静建议孙月教育孩子学会安排时间",
                [
                    ("王静", "看你脸色不太好，是不是昨晚没休息好？"),
                    ("孙月", "别提了。我女儿昨晚做作业又做到11点。"),
                    ("王静", "睡觉太晚对孩子的身体没有好处。最近孩子作业是不是太多了？"),
                    ("孙月", "主要是她做事情比较慢，比如早上闹钟响了她不醒，我赶时间送她上学，她又急着上厕所。每天因为这些小事批评她，弄得我俩心情都不好。"),
                    ("王静", "孩子做事慢，往往是因为他们不会安排自己的时间。你应该让孩子学会管理时间。"),
                    ("孙月", "看来还是我的教育方法有问题。平时看她做事情慢，总想替她做，以后得让她学会安排时间，自己的事情自己做。"),
                ],
            ),
        ],
    },
    16: {
        "title": "生活可以更美好",
        "vocab": [
            ("博士", "bóshì", "n. doctor (academic degree)"),
            ("签证", "qiānzhèng", "n. visa"),
            ("报名", "bào míng", "v. to apply, to sign up"),
            ("表格", "biǎogé", "n. form, table"),
            ("传真", "chuánzhēn", "v. to send by fax"),
            ("号码", "hàomǎ", "n. number"),
            ("参观", "cānguān", "v. to visit, to look around"),
            ("激动", "jīdòng", "adj. excited, emotional"),
            ("小伙子", "xiǎohuǒzi", "n. young man"),
            ("记者", "jìzhě", "n. journalist, reporter"),
            ("代表", "dàibiǎo", "v. to represent, to stand for"),
            ("恐怕", "kǒngpà", "adv. I guess..."),
            ("失望", "shīwàng", "v. disappointed"),
            ("郊区", "jiāoqū", "n. suburb, outskirts"),
            ("到底", "dàodǐ", "adv. on earth"),
            ("呀", "ya", "part. used at the end of a question to soften the tone"),
            ("导游", "dǎoyóu", "n. tour guide"),
            ("礼貌", "lǐmào", "n. polite"),
            ("原谅", "yuánliàng", "v. to forgive"),
        ],
        "dialogues": [
            (
                "课文 1",
                "小夏出国留学遇到了问题",
                [
                    ("小雨", "你马上就要硕士毕业了吧？将来有什么打算？"),
                    ("小夏", "我想出国读博士，一直在准备办签证需要的材料。"),
                    ("小雨", "现在材料准备得怎么样了？"),
                    ("小夏", "成绩证明和护照已经准备好了，另外，还跟国外的大学取得了联系，填写了报名表格。"),
                    ("小雨", "还应该有国外大学给你的邀请信吧？他们把邀请信传真给你了吗？"),
                    ("小夏", "没有啊，下个星期我就要去使馆办签证了，这可怎么办？"),
                    ("小雨", "这可是个大问题，我也不太清楚。我帮你查一下学校的电话号码，你打电话问一下吧。"),
                ],
            ),
            (
                "课文 2",
                "王老板告诉李进自己成功的经验",
                [
                    ("李进", "谢谢您带我参观您的公司。在参观过程中我很激动，有个问题一直想问您。"),
                    ("王老板", "好啊！小伙子，咱们一边吃西瓜，一边聊。"),
                    ("李进", "您从大学毕业开始工作，到现在才十年时间，怎么给公司赚了这么多钱？这让我非常吃惊。我想向您学习一下成功的经验。"),
                    ("王老板", "这个问题以前一个记者也问过我。做生意时虽然会遇到各种压力和困难，但是大家的机会都是相同的。你看，这里有三块大小不同的西瓜，我们用西瓜的大小代表钱的多少，要是我们一起开始吃，你会先选哪块？"),
                    ("李进", "我肯定先吃最大的一块了，难道您会先吃小的，放弃吃大块的机会吗？"),
                    ("王老板", "我会先吃最小的一块，因为在你没吃完最大的那块时，我还有时间再多吃一块，最后一定比你吃的西瓜多。听完我的回答，恐怕你已经知道我的答案了吧。"),
                ],
            ),
            (
                "课文 3",
                "小林不好意思拒绝朋友",
                [
                    ("小林", "今年放假我又回不了家了，这次我父母又要失望了。你有什么计划？"),
                    ("小李", "我计划去郊区住一个月。你不是已经买好火车票了吗？你到底怎么打算的呀？"),
                    ("小林", "昨天一个外地的好朋友打电话说要来旅游，让我当导游，我实在不好意思拒绝。"),
                    ("小李", "其实拒绝并不表示不愿意帮忙。遇到解决不了的问题或者无法完成的任务时，拒绝正好说明你对朋友负责。这也是对你父母负责的态度。"),
                    ("小林", "既然别人找我帮忙，说明他真的很需要我的帮助。我担心要是说“不”的话，会让他误会和伤心。"),
                    ("小李", "别担心！如果你用一个既合适又礼貌的方法告诉朋友，他一定会原谅你的。"),
                ],
            ),
        ],
    },
    17: {
        "title": "人与自然",
        "vocab": [
            ("凉快", "liángkuai", "adj. pleasantly cool"),
            ("热闹", "rènao", "adj. busy, bustling"),
            ("植物", "zhíwù", "n. plant"),
            ("广播", "guǎngbō", "n. broadcast, radio"),
            ("专门", "zhuānmén", "adv. specially"),
            ("倒", "dào", "adv. contrary to the fact, yet, actually"),
            ("安娜", "Ānnà", "name of a person"),
            ("马克", "Mǎkè", "name of a person"),
            ("抱", "bào", "v. to hold in the arms, to hug"),
            ("严格", "yángé", "adj. strict, rigorous"),
            ("难受", "nánshòu", "adj. to feel unwell, to suffer pain"),
            ("趟", "tàng", "m. used for a round trip"),
            ("放暑假", "fàng shǔjià", "to have summer vacation"),
            ("老虎", "lǎohǔ", "n. tiger"),
            ("入口", "rùkǒu", "n. entrance"),
            ("排队", "páiduì", "v. to line up"),
            ("活泼", "huópō", "adj. lively, active"),
            ("只", "zhī", "m. for animals"),
            ("友好", "yǒuhǎo", "adj. friendly"),
        ],
        "dialogues": [
            (
                "课文 1",
                "小夏和安娜在聊天气",
                [
                    ("小夏", "最近天气越来越凉快了，风一刮，草地上就会有一层厚厚的黄叶，看来秋天已经到了。"),
                    ("安娜", "这几天香山特别热闹，随着气温的降低，那里许多植物的叶子都由绿变黄或者变红，吸引了很多游客参观，咱们今天也去看看吧。"),
                    ("小夏", "你看天上的云，今天肯定雨大。再说，香山上看红叶的人太多了。咱们改天去长城吧，广播里说那里也有不少专门看红叶的好地方。"),
                    ("安娜", "真可惜，我还想多照点儿香山的照片呢。去长城倒是一个好主意，那我们明天去吧。"),
                    ("小夏", "明天恐怕也不行，明天是我爸的生日。"),
                    ("安娜", "没关系，那我们再约时间。"),
                ],
            ),
            (
                "课文 2",
                "小林和小李在聊小李的狗",
                [
                    ("小林", "你的这只大黑狗毛真漂亮，而且这么聪明，每次见了都想抱一抱它。"),
                    ("小李", "狗是很聪明的动物，只要稍微花点儿时间教教它，它就能学会很多东西。"),
                    ("小林", "听你这么一说，我现在也想养一只狗了。每次你让它干什么，它就像能听懂你的话一样去做。你教它是不是用了什么特别的方法？"),
                    ("小李", "要让它完成一些任务，只教一次是不够的，应该耐心地一遍一遍地教给它，使它熟悉，然后它就会严格按照你的要求做了。"),
                    ("小林", "看来没有想的那么容易。"),
                    ("小李", "狗是我们的好朋友，它能听懂人的话，明白人的心情。在你心里难受的时候，它会一直陪着你。"),
                ],
            ),
            (
                "课文 3",
                "马克和小夏在聊动物",
                [
                    ("马克", "上个月我去了趟北京动物园，那里约有500种动物，听导游说北京动物园是亚洲最大的动物园之一。"),
                    ("小夏", "去年放暑假的时候，我也去过一次，我在那儿看了马、熊猫、老虎等动物。我特别喜欢熊猫，可惜它们当时大都在睡觉。"),
                    ("马克", "我去的那天正赶上六一儿童节，许多父母带着孩子去动物园。入口处排队的人很多，动物园里热闹极了。大熊猫们也变得特别活泼，我还给它们照了不少照片呢。"),
                    ("小夏", "大熊猫身子胖胖的，样子可爱极了。"),
                    ("马克", "不过，它们数量不多，现在全世界一共才有一千多只吧。"),
                    ("小夏", "以前只有中国有大熊猫，为了表示友好，从1957年开始，中国把大熊猫作为礼物送给其他一些国家。现在，很多国家的人们在本国都能看到大熊猫了。"),
                ],
            ),
        ],
    },
    18: {
        "title": "科技与世界",
        "vocab": [
            ("降落", "jiàngluò", "v. to descend, to land"),
            ("火", "huǒ", "adj. hot, popular"),
            ("作者", "zuòzhě", "n. author"),
            ("交通", "jiāotōng", "n. traffic, communication"),
            ("技术", "jìshù", "n. technology"),
            ("是否", "shìfǒu", "adv. if, whether"),
            ("秒", "miǎo", "m. second, 1/60 minute"),
            ("方式", "fāngshì", "n. way, mode"),
            ("受不了", "shòubuliǎo", "cannot stand, cannot bear"),
            ("日记", "rìjì", "n. diary, journal"),
            ("安全", "ānquán", "adj. safe, secure"),
            ("密码", "mìmǎ", "n. password"),
            ("允许", "yǔnxǔ", "v. to allow, to permit"),
            ("座", "zuò", "m. used for bridges, mountains, buildings, etc."),
            ("桥", "qiáo", "n. bridge"),
            ("危险", "wēixiǎn", "adj. dangerous"),
            ("接着", "jiēzhe", "adv. then, immediately after that"),
            ("警察", "jǐngchá", "n. police"),
            ("抓", "zhuā", "v. to catch, to arrest"),
            ("咸", "xián", "adj. salty"),
            ("矿泉水", "kuàngquánshuǐ", "n. mineral water"),
        ],
        "dialogues": [
            (
                "课文 1",
                "王静给孙月推荐一本书",
                [
                    ("孙月", "上次女儿问我飞机是怎么起飞和降落的，真不知道该怎么回答她，她现在总是有各种各样的“为什么”。"),
                    ("王静", "孩子眼中的世界是美丽和奇特的。有一本书叫《新十万个为什么》，现在卖得非常火。书里的内容都是儿童想知道的科学知识，相信你女儿一定喜欢读。"),
                    ("孙月", "难道它和我们小时候看的《十万个为什么》不一样吗？作者是谁啊？"),
                    ("王静", "作者的名字我没记住。《新十万个为什么》的内容更新，介绍了各种科学知识，包括地球、动物、植物、交通、科学技术、社会和文化等很多方面。"),
                    ("孙月", "太好了！不过她这么小，我不知道她是否能读懂。"),
                    ("王静", "放心吧，这本书的语言简单易懂，一定能增长孩子的科学知识。"),
                ],
            ),
            (
                "课文 2",
                "李老师和高老师在聊电脑和互联网技术的发展",
                [
                    ("李老师", "现在的大学生一遇到不明白的问题，可以马上在网上查找答案，几秒钟就把问题解决了，这比我们上学的时候方便多了。"),
                    ("高老师", "现在的人们，尤其是大学生开始普遍使用电脑，他们的生活已经离不开电脑。据调查，70%的人遇到问题时，首先想到的就是上网找答案。"),
                    ("李老师", "电脑和互联网技术的发展使学生们的学习方式发生了很多变化，不过天天对着电脑看，眼睛实在受不了。"),
                    ("高老师", "不仅是学习方式，而且连生活方式也发生了很大改变。现在越来越多的学生喜欢在网上写日记，他们说这样可以让朋友及时了解自己的生活。"),
                    ("李老师", "这个办法不错，既能方便大家的交流，还能节约用纸，保护环境。但是如果别人都能看到我的日记的话，多不安全啊！"),
                    ("高老师", "放心吧，可以给网上的日记加密码，那样只有得到了允许，别人才能看到。"),
                ],
            ),
            (
                "课文 3",
                "王静和孙月在聊关于梦的情况",
                [
                    ("王静", "我昨天晚上做了一个特别奇怪的梦，梦到自己正在一座桥上走，走着走着，突然开过来一辆车，非常危险，接着又梦见我跳到车上，跟警察一起抓住了一个坏人。"),
                    ("孙月", "奇怪，你怎么总能记住自己做了什么梦？我好像从来没做过梦。"),
                    ("王静", "每个人都会做梦，区别只是有多有少。有的人睡醒之后还记得梦里的事情，有的人却记不清楚了。你之所以觉得从来没做过梦，只不过是忘记了。"),
                    ("孙月", "你说的有道理，我一般都是一觉睡到天亮。很多人认为做梦是上天要告诉他们将来会发生的一些事情，可能上天不想让我知道吧。"),
                    ("王静", "一般晚上睡觉时，身体感觉到什么，人就容易梦到什么内容。记得有一次，我晚饭吃得太咸，那天晚上就梦见自己到处找商店买矿泉水。"),
                    ("孙月", "很多人都试着对梦进行解释，有些人甚至专门写过这方面的书，可惜到现在仍然没有一个科学的说法。"),
                ],
            ),
        ],
    },
    19: {
        "title": "生活的味道",
        "vocab": [
            ("学期", "xuéqī", "n. term, semester"),
            ("出生", "chūshēng", "v. to be born"),
            ("性别", "xìngbié", "n. sex, gender"),
            ("道歉", "dào qiàn", "v. to apologize"),
            ("打印", "dǎyìn", "v. to print out"),
            ("复印", "fùyìn", "v. to photocopy, to xerox"),
            ("饺子", "jiǎozi", "n. jiaozi, dumpling"),
            ("刀", "dāo", "n. knife"),
            ("破", "pò", "adj. broken, torn"),
            ("脱", "tuō", "v. to take off"),
            ("理发", "lǐfà", "v. to get a haircut"),
            ("包子", "bāozi", "n. steamed stuffed bun"),
            ("零钱", "língqián", "n. small change"),
            ("打招呼", "dǎ zhāohu", "to greet, to say hello"),
            ("戴", "dài", "v. to wear accessories"),
            ("眼镜", "yǎnjìng", "n. glasses, spectacles"),
            ("舞蹈", "wǔdǎo", "n. dance"),
            ("国籍", "guójí", "n. nationality, citizenship"),
            ("抬", "tái", "v. to lift, to raise"),
            ("胳膊", "gēbo", "n. arm"),
            ("转", "zhuǎn", "v. to turn, to shift"),
        ],
        "dialogues": [
            (
                "课文 1",
                "马克申请下个学期继续在学校学习",
                [
                    ("马克", "老师，您好！我希望下个学期在这里继续学习，请问还需要重新申请吗？"),
                    ("高老师", "是的。给你表格，出生年月、性别、护照号码都要填，还有联系地址、联系电话。"),
                    ("马克", "真抱歉，我不小心把护照号码填错了，您能再给我一份新的申请表吗？"),
                    ("高老师", "没关系，不用道歉，谁都有粗心填错的时候。申请表都被别人拿走了，我给你重新打印一份，你等一下。"),
                    ("旁白", "（高老师打印，马克填表。）"),
                    ("马克", "这次我按照要求都填写完了，请问还需要做别的事情吗？"),
                    ("高老师", "请把你的护照给我，我们要把护照复印一下。"),
                ],
            ),
            (
                "课文 2",
                "王静做饺子时手受伤了",
                [
                    ("李进", "呀，你的手怎么流血了？等一下，我给你包起来。"),
                    ("王静", "没关系，我想给你做点儿羊肉饺子，刚才用刀切肉的时候把手弄破了。"),
                    ("李进", "你也太不小心了，不过好像不太严重，过几天就好了。衣服上也有一点儿血，你把衣服脱下来，我给你洗洗。"),
                    ("王静", "看来今天吃不上羊肉饺子了。"),
                    ("李进", "那我们就吃点儿别的。我常去的那家理发店附近有个餐厅，那里的包子很好吃，我一会儿去买一点儿。"),
                    ("王静", "好吧，我衣服口袋里有十几块零钱，买包子应该够。"),
                ],
            ),
            (
                "课文 3",
                "安娜帮助马克练习舞蹈动作",
                [
                    ("马克", "我早上跟你打招呼，你没看见。想不到又在这儿碰见你了。"),
                    ("安娜", "真是对不起，我不是故意的，今天早上我忘戴眼镜了，看不清楚。"),
                    ("马克", "刚才我在旁边看到你跳中国舞了，没看出来你跳得这么好！难道你以前在你们国家就学过中国舞蹈吗？"),
                    ("安娜", "我小时候妈妈教我跳过两年的舞，所以稍微有点儿基础。再说，舞蹈不仅是一门艺术，也是一种“语言”，这种语言与国籍无关，无论哪个国家的人都能看懂。"),
                    ("马克", "太好了！我刚学习跳这种舞没多久，你帮我看看，我的这个动作对不对。"),
                    ("安娜", "你这个动作做得还是不太标准，我给你跳一遍。你仔细看着，应该像我这样：先抬胳膊，然后抬腿，最后头再向右转一下。"),
                ],
            ),
        ],
    },
    20: {
        "title": "路上的风景",
        "vocab": [
            ("加油站", "jiāyóuzhàn", "n. gas station"),
            ("航班", "hángbān", "n. scheduled flight"),
            ("推迟", "tuīchí", "v. to postpone, to delay"),
            ("高速公路", "gāosù gōnglù", "expressway"),
            ("登机牌", "dēngjīpái", "n. boarding pass"),
            ("首都", "shǒudū", "n. capital of a country"),
            ("旅行", "lǚxíng", "v. to travel, to tour"),
            ("怪", "guài", "adv. rather, quite"),
            ("可怜", "kělián", "adj. pitiable, poor"),
            ("对面", "duìmiàn", "n. opposite, across"),
            ("烤鸭", "kǎoyā", "n. roast duck"),
            ("祝贺", "zhùhè", "v. to congratulate"),
            ("合格", "hégé", "adj. qualified, up to standard"),
            ("干杯", "gān bēi", "v. to drink a toast"),
            ("民族", "mínzú", "n. nationality, ethnic group"),
            ("打扮", "dǎban", "v. to dress up, to deck out"),
            ("笑话", "xiàohua", "n. joke"),
            ("存", "cún", "v. to store, to keep"),
            ("钥匙", "yàoshi", "n. key"),
            ("究竟", "jiūjìng", "adv. used in questions for emphasis; exactly"),
        ],
        "dialogues": [
            (
                "课文 1",
                "小张去北京，朋友送小张去机场",
                [
                    ("朋友", "该加油了，去机场的路上有加油站吗？"),
                    ("小张", "我记得过了长江大桥往右一拐就有一个，大概有四五公里远。"),
                    ("朋友", "好，那我就放心了，别开着开着没油了。你去北京的航班是几点的？时间来得及吗？"),
                    ("小张", "航班本来是10点的，后来机场网站上通知推迟了一个小时，所以9点半以前到就应该没问题。"),
                    ("朋友", "刚才我还有点儿担心来不及呢。一会儿加完油，往西走五百米就能上高速公路。走高速公路大约半个小时就到了。"),
                    ("小张", "一会儿我自己进去换登机牌，你就不用送我了，等我到了首都机场再给你发短信。"),
                ],
            ),
            (
                "课文 2",
                "孙月和丈夫计划放寒假带女儿去旅行",
                [
                    ("孙月", "女儿下个星期就要放寒假了，到时候咱们带她去旅游，放松放松，怎么样？"),
                    ("丈夫", "平时女儿那么多课，总是说想去旅行，但是没时间，怪可怜的。这次放假咱们带她去哪儿玩儿比较好呢？"),
                    ("孙月", "去年我同事带她儿子去广西玩儿了一趟，听说很不错，我们就去广西吧。"),
                    ("丈夫", "好啊，那里的气候和北方很不同，即使是冬天，也非常暖和，还能吃到许多新鲜的水果。等女儿一回来我就告诉她这个好消息。"),
                    ("孙月", "先别着急说。中午我们不是要去对面的饭店吃烤鸭，祝贺她考试成绩都合格吗？那时候再告诉她，不是更好？"),
                    ("丈夫", "好主意，到时她知道了肯定特别开心。"),
                ],
            ),
            (
                "课文 3",
                "安娜向马克介绍去丽江旅行的经验",
                [
                    ("马克", "这么多照片，都是你这次去丽江旅行时照的？那里的自然风景可真美！"),
                    ("安娜", "是啊，小城四季的风景都很美，而且环境保护得也很好，因此每年都吸引着成千上万的游客去那儿旅游。"),
                    ("马克", "这张照片上和你干杯的那个人是少数民族吗？她打扮得真漂亮。"),
                    ("安娜", "她是我们的导游，不是少数民族。一路上她给我们讲了很多有趣的笑话。有一次我把存包的钥匙丢了，最后还是她帮我找到的。这张照片就是找到钥匙后，我们一起照的。"),
                    ("马克", "明年我有机会也去那儿看看，到时把你的导游介绍给我吧。究竟哪个季节去丽江旅游比较好呢？"),
                    ("安娜", "那儿最美的季节是春天和秋天，不过那时候人比较多。稍微好一点儿的时间是每年12月到第二年3月。这段时间去丽江的话，无论交通还是吃、住都很便宜。"),
                ],
            ),
        ],
    },
}


VOCAB_UZ = {
    "规定": "qoida, tartib",
    "死": "qattiq, moslashmaydigan",
    "可惜": "afsus, achinarli",
    "全部": "hammasi, butun",
    "也许": "balki, ehtimol",
    "商量": "maslahatlashmoq, muhokama qilmoq",
    "并且": "va, shuningdek",
    "盐": "tuz",
    "勺（子）": "qoshiq",
    "保护": "himoya qilmoq",
    "作用": "vazifa, ta'sir",
    "无法": "qila olmaslik, imkonsiz bo'lmoq",
    "节": "bo'lim, qism",
    "详细": "batafsil",
    "解释": "tushuntirmoq",
    "对于": "...ga nisbatan, ...haqida",
    "叶子": "barg",
    "教育": "ta'lim bermoq, tarbiya bermoq",
    "京剧": "Pekin operasi",
    "演员": "aktyor, aktrisa",
    "观众": "tomoshabinlar",
    "厚": "chuqur, mustahkam",
    "演出": "sahnaga chiqmoq, ijro etmoq",
    "大概": "taxminan, chamasi",
    "来自": "...dan kelmoq, ...dan bo'lmoq",
    "遍": "marta, boshidan oxirigacha bir bor",
    "偶尔": "ba'zan, onda-sonda",
    "吃惊": "hayron qolmoq, ajablanmoq",
    "基础": "asos, poydevor",
    "表演": "ijro etmoq, namoyish qilmoq",
    "出差": "xizmat safariga bormoq",
    "毛巾": "sochiq",
    "牙膏": "tish pastasi",
    "重": "og'ir",
    "行": "bo'ladi, mayli",
    "省": "tejamoq",
    "污染": "ifloslantirmoq",
    "卫生间": "hojatxona, yuvinish xonasi",
    "脏": "kir, iflos",
    "抱歉": "kechirim so'ramoq, uzr",
    "空": "bo'sh",
    "盒子": "quti",
    "扔": "tashlab yubormoq",
    "以": "...orqali, ...vositasida",
    "速度": "tezlik",
    "地球": "Yer, yer shari",
    "既然": "modomiki, shunday ekan",
    "停": "to'xtamoq",
    "得意": "o'zidan mamnun, kerilib ketgan",
    "目的": "maqsad",
    "暖": "iliq",
    "弹钢琴": "pianino chalmoq",
    "棒": "zo'r, ajoyib",
    "孙子": "nevara o'g'il",
    "寒假": "qishki ta'til",
    "父亲": "ota",
    "闹钟": "budilnik",
    "响": "jiringlamoq, ovoz chiqarmoq",
    "醒": "uyg'onmoq",
    "赶": "shoshilmoq, ulgurishga harakat qilmoq",
    "厕所": "hojatxona",
    "批评": "tanqid qilmoq",
    "弄": "qilmoq, qilib qo'ymoq",
    "管理": "boshqarmoq",
    "博士": "doktorantura/doktor ilmiy darajasi",
    "签证": "viza",
    "报名": "ro'yxatdan o'tmoq, ariza bermoq",
    "表格": "jadval, anketa",
    "传真": "faks orqali yubormoq",
    "号码": "raqam",
    "参观": "tomosha qilmoq, ko'rib chiqmoq",
    "激动": "hayajonlangan",
    "小伙子": "yigit",
    "记者": "jurnalist, muxbir",
    "代表": "ifodalamoq, vakillik qilmoq",
    "恐怕": "ehtimol, qo'rqamanki",
    "失望": "hafsalasi pir bo'lmoq",
    "郊区": "shahar cheti",
    "到底": "aslida, axir",
    "呀": "gap oxirida ohangni yumshatuvchi yuklama",
    "导游": "gid, ekskursovod",
    "礼貌": "odobli, muloyim",
    "原谅": "kechirmoq",
    "凉快": "salqin, yoqimli salqin",
    "热闹": "gavjum, jonli",
    "植物": "o'simlik",
    "广播": "radio, eshittirish",
    "专门": "maxsus",
    "倒": "aksincha, baribir, ...-ku",
    "安娜": "Anna",
    "马克": "Mark",
    "抱": "quchoqlamoq",
    "严格": "qat'iy, talabchan",
    "难受": "qiynalmoq, o'zini yomon his qilmoq",
    "趟": "borib-kelish marta",
    "放暑假": "yozgi ta'tilga chiqmoq",
    "老虎": "yo'lbars",
    "入口": "kirish joyi",
    "排队": "navbatda turmoq",
    "活泼": "sho'x, faol",
    "只": "hayvonlar uchun dona hisob so'zi",
    "友好": "do'stona",
    "降落": "qo'nmoq, pasaymoq",
    "火": "mashhur, juda ommabop",
    "作者": "muallif",
    "交通": "transport, qatnov",
    "技术": "texnologiya, texnika",
    "是否": "mi yoki yo'qmi",
    "秒": "soniya",
    "方式": "usul, yo'l",
    "受不了": "chidab bo'lmaslik",
    "日记": "kundalik",
    "安全": "xavfsiz",
    "密码": "parol",
    "允许": "ruxsat bermoq",
    "座": "bino/ko'prik/tog' uchun hisob so'zi",
    "桥": "ko'prik",
    "危险": "xavfli",
    "接着": "keyin, darhol so'ng",
    "警察": "politsiya",
    "抓": "ushlamoq, qo'lga olmoq",
    "咸": "sho'r",
    "矿泉水": "mineral suv",
    "学期": "semestr, o'quv davri",
    "出生": "tug'ilmoq",
    "性别": "jins",
    "道歉": "kechirim so'ramoq",
    "打印": "printerdan chiqarmoq",
    "复印": "nusxa ko'chirmoq",
    "饺子": "jiaozi, chuchvara",
    "刀": "pichoq",
    "破": "yirtilgan, singan",
    "脱": "yechmoq",
    "理发": "soch oldirmoq",
    "包子": "baozi, bug'da pishgan somsa",
    "零钱": "mayda pul",
    "打招呼": "salomlashmoq",
    "戴": "taqmoq, kiyib olmoq",
    "眼镜": "ko'zoynak",
    "舞蹈": "raqs",
    "国籍": "fuqarolik, millat",
    "抬": "ko'tarmoq",
    "胳膊": "qo'l, bilak",
    "转": "burilmoq, aylantirmoq",
    "加油站": "yoqilg'i quyish shoxobchasi",
    "航班": "aviaqatnov, reys",
    "推迟": "kechiktirmoq",
    "高速公路": "tezkor avtomagistral",
    "登机牌": "samolyotga chiqish taloni",
    "首都": "poytaxt",
    "旅行": "sayohat qilmoq",
    "怪": "ancha, juda",
    "可怜": "bechora, achinarli",
    "对面": "qarshi tomon, ro'para",
    "烤鸭": "qovurilgan o'rdak",
    "祝贺": "tabriklamoq",
    "合格": "talabga javob beradigan",
    "干杯": "qadah ko'tarmoq",
    "民族": "millat, etnik guruh",
    "打扮": "bezantirmoq, yasatmoq",
    "笑话": "hazil",
    "存": "saqlamoq",
    "钥匙": "kalit",
    "究竟": "aslida, aynan",
}


SCENE_UZ = {
    "王经理做生意遇到了困难": "Wang menejer biznesda qiyinchilikka duch keldi",
    "高老师告诉女儿洗衣服的方法": "Gao o'qituvchi qiziga kiyim yuvish usulini aytmoqda",
    "高老师学习王教授的教育方法": "Gao o'qituvchi professor Wangning ta'lim usulini o'rganmoqda",
    "小雨和小夏在聊小夏的爷爷表演京剧的情况": "Xiaoyu va Xiaoxia bobosining Pekin operasi ijrosi haqida gaplashmoqda",
    "小雨和马克在聊京剧": "Xiaoyu va Mark Pekin operasi haqida gaplashmoqda",
    "李进要出差，王静和李进在聊天儿": "Li Jin xizmat safariga chiqmoqchi, Wang Jing bilan gaplashmoqda",
    "经理和服务员在谈工作": "Menejer va ofitsiant ish haqida gaplashmoqda",
    "孙月和王静在聊关于环保的事情": "Sun Yue va Wang Jing ekologiya haqida gaplashmoqda",
    "李老师建议王静让孩子养成好习惯": "Li o'qituvchi Wang Jingga bolada yaxshi odat shakllantirishni maslahat bermoqda",
    "王静建议孙月教育孩子学会安排时间": "Wang Jing Sun Yuega bolani vaqtni rejalashga o'rgatishni maslahat bermoqda",
    "小夏出国留学遇到了问题": "Xiaoxia chet elda o'qish masalasida muammoga duch keldi",
    "王老板告诉李进自己成功的经验": "Wang boshliq Li Jinga muvaffaqiyat tajribasini aytmoqda",
    "小林不好意思拒绝朋友": "Xiaolin do'stini rad etishga uyalmoqda",
    "小夏和安娜在聊天气": "Xiaoxia va Anna ob-havo haqida gaplashmoqda",
    "小林和小李在聊小李的狗": "Xiaolin va Xiaoli Xiaolining iti haqida gaplashmoqda",
    "马克和小夏在聊动物": "Mark va Xiaoxia hayvonlar haqida gaplashmoqda",
    "王静给孙月推荐一本书": "Wang Jing Sun Yuega kitob tavsiya qilmoqda",
    "李老师和高老师在聊电脑和互联网技术的发展": "Li o'qituvchi va Gao o'qituvchi kompyuter va internet rivoji haqida gaplashmoqda",
    "王静和孙月在聊关于梦的情况": "Wang Jing va Sun Yue tushlar haqida gaplashmoqda",
    "马克申请下个学期继续在学校学习": "Mark keyingi semestr ham maktabda o'qish uchun ariza bermoqda",
    "王静做饺子时手受伤了": "Wang Jing jiaozi qilayotganda qo'lini jarohatladi",
    "安娜帮助马克练习舞蹈动作": "Anna Markga raqs harakatlarini mashq qilishda yordam bermoqda",
    "小张去北京，朋友送小张去机场": "Xiao Zhang Pekinga ketmoqda, do'sti uni aeroportga olib bormoqda",
    "孙月和丈夫计划放寒假带女儿去旅行": "Sun Yue va eri qishki ta'tilda qizini sayohatga olib borishni rejalashmoqda",
    "安娜向马克介绍去丽江旅行的经验": "Anna Markga Lijiang sayohati tajribasini aytmoqda",
}


GRAMMAR_TITLES = {
    12: ["并且", "再……也……", "对于"],
    13: ["大概", "着", "由", "进行", "随着"],
    14: ["够", "以", "既然", "于是", "什么的"],
    15: ["想起来", "弄", "千万", "来", "左右"],
    16: ["了", "乱", "到底", "拿……来说", "趁"],
    17: ["倒", "下", "想", "为了……而……", "仍然"],
    18: ["是否", "方式", "受不了", "只有……才……"],
    19: ["疑问代词活用表示任指"],
    20: ["V着V着", "一边……一边……", "先", "起来", "V着"],
}


DIALOGUE_UZ = {
    "听说这次生意你到现在还没谈成。": "Eshitishimcha, bu safargi kelishuvni haligacha yakunlamabsiz.",
    "按我以前的经验，早应该谈成了，这次我也不知道哪儿出了问题。": "Oldingi tajribamga ko'ra, allaqachon kelishilgan bo'lishi kerak edi, bu safar qayerda muammo chiqqanini bilmayapman.",
    "有句话叫“规定和经验是死的，人是活的”。当“规定”和“经验”不能解决问题时，建议你改变一下自己的态度和想法。": "Bir gap bor: “qoidalar va tajriba qotib qolgan, odam esa moslasha oladi”. Qoidalar va tajriba muammoni hal qilolmasa, munosabat va fikringizni biroz o'zgartiring.",
    "很多时候，我都习惯根据过去的经验做事，可惜，经验不是全部都是对的。": "Ko'p hollarda ishni eski tajribaga tayanib qilaman, afsuski, hamma tajriba ham to'g'ri bo'lavermaydi.",
    "遇到不能解决的问题时，我们应该试着走走以前从来没走过的路，也许这样就能找到解决问题的方法了。": "Hal qilib bo'lmayotgan muammoga duch kelsak, avval yurmagan yo'ldan borib ko'rish kerak, balki shunda yechim topilar.",
    "好，我再跟同事商量商量，希望能及时发现问题，并且准确地找到解决问题的方法。": "Yaxshi, hamkasblarim bilan yana maslahatlashaman, muammoni vaqtida topib, aniq yechim topamiz deb umid qilaman.",
    "妈，您看我刚买的裤子，洗完以后颜色怎么变得这么难看呢？": "Oyi, qarang, yangi olgan shimimni yuvgandan keyin rangi nega bunday xunuk bo'lib qoldi?",
    "看来是掉颜色了，你洗的时候在水里加点儿盐就不会这样了。": "Rangi ketganga o'xshaydi. Yuvayotganda suvga ozgina tuz qo'shsang, bunday bo'lmaydi.",
    "放盐？！盐不是用来做饭的吗？难道它还能让衣服不掉颜色？": "Tuz solish?! Tuz ovqat qilish uchun emasmi? Nahotki kiyim rangini saqlasa?",
    "当然。有些衣服第一次洗的时候会掉颜色，其实，有很多方法可以解决这个问题。在水里加勺盐再洗是最简单的方法。用盐水来洗新衣服，这样穿得再久、洗的次数再多，衣服也不容易掉颜色。": "Albatta. Ba'zi kiyimlar birinchi yuvilganda rang beradi. Bu muammoni hal qilishning ko'p usuli bor. Suvga bir qoshiq tuz qo'shib yuvish eng oddiy usul. Yangi kiyimni tuzli suvda yuvsang, uzoq kiysang ham, ko'p yuvsang ham rangi oson ketmaydi.",
    "我第一次听说盐有保护衣服颜色的作用，生活中还真有不少课本上无法学到的知识。": "Tuz kiyim rangini himoya qilishini birinchi marta eshitdim. Hayotda darslikdan o'rganib bo'lmaydigan bilimlar ko'p ekan.",
    "实际上，很多问题的答案都可以从生活中找到。但这需要你用眼睛去发现，用心去总结。": "Aslida ko'p savollarning javobini hayotdan topish mumkin. Buning uchun ko'z bilan kuzatish va qalb bilan xulosa qilish kerak.",
    "王教授，今天听完您的这节课，我终于明白为什么您的课那么受学生欢迎了。": "Professor Wang, bugun darsingizni tinglab, nega darslaringiz talabalar orasida bunchalik mashhur ekanini tushundim.",
    "谢谢！您能详细谈谈对我的课的看法吗？": "Rahmat! Darsim haqidagi fikringizni batafsil ayta olasizmi?",
    "我发现您对学生特别了解，而且总是能用最简单的方法把复杂的问题解释清楚，让每个学生都能听懂，这一点真是值得我们好好儿学习。": "Siz talabalarni juda yaxshi tushunar ekansiz, murakkab masalalarni eng sodda usulda tushuntirib, har bir talaba anglaydigan qilasiz. Bu biz o'rganishimiz kerak bo'lgan jihat.",
    "哪里哪里，这只是因为我对每个学生的能力水平比较了解。": "Yo'g'e, bu shunchaki har bir talabaning qobiliyat darajasini yaxshi bilganim uchun.",
    "那您认为对于老师来说，什么是最难做到的？": "Sizningcha, o'qituvchi uchun eng qiyini nima?",
    "世界上没有完全相同的叶子，同样地，世界上也没有完全一样的人。所以，在教育学生时，要根据学生的特点选择不同的方法，我想这应该是最不容易做到的。": "Dunyoda mutlaqo bir xil barg yo'q, xuddi shunday mutlaqo bir xil odam ham yo'q. Shuning uchun talabani o'qitishda uning xususiyatiga qarab turli usul tanlash kerak. Menimcha, eng qiyini shu.",
    "小夏，你爷爷京剧唱得真专业，我还以为他是京剧演员呢。": "Xiaoxia, bobongiz Pekin operasini juda professional kuylarkan, uni aktyor deb o'ylabman.",
    "对啊，他本来就是京剧演员，年轻时在我们那儿很有名，深受观众们的喜爱。": "Ha, u aslida Pekin operasi aktyori. Yoshligida biz tomonda juda mashhur bo'lgan, tomoshabinlar uni yaxshi ko'rishgan.",
    "你爷爷一定对京剧有着很深厚的感情。": "Bobongiz Pekin operasiga juda chuqur mehr qo'ygan bo'lsa kerak.",
    "是呀，他8岁就开始上台演出，到现在大概唱了60多年了，他对这门艺术的喜爱从来没有改变过。": "Ha, u 8 yoshida sahnaga chiqa boshlagan, hozirgacha taxminan 60 yildan beri kuylaydi. Bu san'atga bo'lgan muhabbati hech o'zgarmagan.",
    "这么说你喜欢听京剧也是受了你爷爷的影响？": "Demak, Pekin operasini yoqtirishingizga ham bobongiz ta'sir qilganmi?",
    "我小时候经常去看他的演出。平时他还给我讲很多京剧里的历史故事，让我学到了很多知识。": "Bolaligimda uning chiqishlarini ko'p ko'rardim. U menga Pekin operasidagi tarixiy hikoyalarni ham ko'p aytib berardi, shundan ko'p narsa o'rgandim.",
    "真没想到你一个来自美国的外国留学生，能把京剧唱得这么好。": "Amerikadan kelgan chet ellik talaba Pekin operasini bunchalik yaxshi kuylaydi deb o'ylamagandim.",
    "我常常跟着电视学唱京剧，然后一遍一遍地练习，偶尔跟中国人一起唱上几句。": "Men ko'pincha televizorga qo'shilib Pekin operasini o'rganaman, keyin qayta-qayta mashq qilaman, ba'zan xitoyliklar bilan bir-ikki jumla kuylayman.",
    "难道你从来没有接受过京剧方面的专门教育吗？": "Nahotki Pekin operasi bo'yicha maxsus ta'lim olmagan bo'lsangiz?",
    "别吃惊，因为我以前学习过音乐，有一些音乐基础，又对京剧这种表演艺术非常感兴趣，所以能比较容易地学会它的唱法。": "Hayron bo'lmang, men avval musiqa o'rganganman, ozroq asosim bor. Pekin operasi kabi ijro san'atiga juda qiziqqanim uchun uning kuylash usulini nisbatan oson o'rgandim.",
    "你真厉害！竟然连很多中国人都听不懂的京剧也能学会。我还是比较喜欢听流行音乐。": "Zo'rsiz! Hatto ko'p xitoyliklar ham tushunmaydigan Pekin operasini o'rganibsiz. Men esa ko'proq pop musiqa tinglashni yoqtiraman.",
    "那是你不了解京剧的唱法。在音乐方面，京剧给了我很多新的想法。我还把京剧的一些特点增加到了自己的音乐中，达到了很好的效果。": "Bu siz Pekin operasining kuylash usulini yaxshi bilmaganingiz uchun. Musiqada Pekin operasi menga ko'p yangi fikr berdi. Uning ba'zi xususiyatlarini o'z musiqamga qo'shib, yaxshi natijaga erishdim.",
    "这是明天你出差要带的毛巾、牙膏和牙刷，把它们放到箱子里吧。": "Bu ertaga xizmat safariga olib ketadigan sochiq, tish pastasi va tish cho'tkangiz, ularni chamadonga solib qo'ying.",
    "不用拿这些，宾馆都会免费提供的。再说，箱子已经够重的了！": "Bularni olish shart emas, mehmonxona bepul beradi. Ustiga-ustak chamadon allaqachon ancha og'ir!",
    "我当然知道宾馆里有。你不是一直说要保护环境吗？现在就从身边的小事做起吧。": "Mehmonxonada borligini bilaman. Siz doim atrof-muhitni himoya qilish kerak derdingiz-ku? Endi yonimizdagi kichik ishlardan boshlaylik.",
    "行，没问题。我明天上午10点的飞机，你能开车把我送到机场吗？": "Mayli, muammo yo'q. Ertaga ertalab soat 10 dagi reysim bor, meni mashinada aeroportga olib bora olasizmi?",
    "那个时间路上堵车多严重啊！你还是坐地铁去机场吧。这样不仅省油钱，而且还不会污染空气。": "U paytda yo'lda tirbandlik juda kuchli bo'ladi! Yaxshisi aeroportga metroda boring. Bu nafaqat benzin pulini tejaydi, balki havoni ham ifloslantirmaydi.",
    "好，那就听你的。": "Yaxshi, unda aytganingizcha qilaman.",
    "小王，卫生间怎么那么脏啊？这会给客人留下不好的印象，快去打扫一下。": "Xiao Wang, hojatxona nega buncha kir? Bu mijozlarda yomon taassurot qoldiradi, tez borib tozalang.",
    "经理，实在抱歉。今天店里太忙了，我还没来得及打扫。": "Menejer, rostdan uzr. Bugun do'kon juda band bo'ldi, hali tozalashga ulgurmadim.",
    "那张桌子下面还有一些空饮料瓶子和纸盒子。": "Ana u stol tagida ham bo'sh ichimlik shishalari va qog'oz qutilar bor.",
    "好的，我马上就去把它们扔掉。": "Yaxshi, hozir borib ularni tashlab yuboraman.",
    "以后你一定得注意这个问题，不管客人多不多，生意多忙，我们都要保证餐厅干净卫生。": "Bundan keyin bu masalaga albatta e'tibor bering. Mijoz ko'pmi-kammi, ish bandmi, restoran toza va ozoda bo'lishi shart.",
    "经理您放心，我一定以最快的速度完成。不过咱们真的应该再多招聘几个服务员了。": "Xavotir olmang, eng tez suratda bajaraman. Lekin rostdan yana bir nechta ofitsiant ishga olishimiz kerak.",
    "早上听新闻说明天有一个叫“地球一小时”的活动，你对这个活动了解吗？": "Ertalab yangiliklarda ertaga “Yer soati” degan tadbir bo'lishini aytishdi. Bu tadbir haqida bilasizmi?",
    "这个活动年年都有，最早是从2007年开始的。明天晚上很多人都会关灯一小时，支持这个活动。你没看到门口的通知吗？我们公司也参加。": "Bu tadbir har yili bo'ladi, ilk bor 2007 yilda boshlangan. Ertaga kechqurun ko'p odamlar bir soatga chiroqni o'chirib, tadbirni qo'llab-quvvatlaydi. Eshik oldidagi e'lonni ko'rmadingizmi? Bizning kompaniya ham qatnashadi.",
    "真的吗？太好了！既然明天晚上公司会关灯停电，那么我们肯定不用加班了。": "Rostdanmi? Juda yaxshi! Ertaga kechqurun kompaniyada chiroqlar o'chsa, demak aniq qo'shimcha ishlamaymiz.",
    "看你得意的样子！还以为你高兴是为了支持环保，原来是因为不用加班啊！": "Qarang, qanday xursandsiz! Men ekologiyani qo'llab-quvvatlaganingizdan xursandsiz deb o'ylagandim, aslida qo'shimcha ish yo'qligi uchun ekan!",
    "环境保护我当然也支持了！对了，为什么会有这么一个活动啊？": "Atrof-muhitni himoya qilishni albatta qo'llab-quvvatlayman! Aytgancha, nega bunday tadbir bor?",
    "其实目的挺简单的，就是提醒人们节约用电，希望引起人们对气候变暖问题的关注。": "Aslida maqsadi juda oddiy: odamlarga elektrni tejashni eslatish va iqlim isishi muammosiga e'tibor qaratish.",
    "那个一边弹钢琴一边唱歌的男孩子是谁？表演得真棒！": "Pianino chalib, qo'shiq aytayotgan bola kim? Juda zo'r ijro etdi!",
    "是我孙子。去年寒假前的新年晚会他也表演过一次。": "Mening nevaram. O'tgan yili qishki ta'til oldidagi yangi yil kechasida ham bir marta chiqish qilgan.",
    "我想起来了，这孩子又聪明又可爱，你们教育得真好！": "Esimga tushdi, bu bola juda aqlli va yoqimtoy, uni juda yaxshi tarbiyalabsizlar!",
    "是他父母教育得好。父母是孩子最重要的老师。他父母不仅教他知识，而且还花了很长时间帮助他养成了非常好的习惯，现在他每天都自己练习弹钢琴。": "Uni ota-onasi yaxshi tarbiyalagan. Ota-ona bolaning eng muhim o'qituvchisi. Ular unga nafaqat bilim bergan, balki yaxshi odat shakllantirishiga ham ko'p vaqt sarflagan. Hozir u har kuni o'zi pianino mashq qiladi.",
    "让孩子养成一个好习惯实在太重要了，看来我得向他父母好好儿学习。": "Bolada yaxshi odat shakllantirish juda muhim ekan. Men uning ota-onasidan yaxshi o'rganishim kerak.",
    "对。如果希望有一个优秀的孩子，你就要先成为一位优秀的父亲或者母亲。": "To'g'ri. Ajoyib farzand bo'lishini istasangiz, avval o'zingiz ajoyib ota yoki ona bo'lishingiz kerak.",
    "看你脸色不太好，是不是昨晚没休息好？": "Yuzingiz yaxshi ko'rinmayapti, kecha yaxshi dam olmadingizmi?",
    "别提了。我女儿昨晚做作业又做到11点。": "Aytmang. Qizim kecha yana uy vazifasini soat 11 gacha qildi.",
    "睡觉太晚对孩子的身体没有好处。最近孩子作业是不是太多了？": "Juda kech uxlash bola sog'lig'iga foydali emas. So'nggi payt uy vazifasi ko'payib ketdimi?",
    "主要是她做事情比较慢，比如早上闹钟响了她不醒，我赶时间送她上学，她又急着上厕所。每天因为这些小事批评她，弄得我俩心情都不好。": "Asosiysi, u ishni sekin qiladi. Masalan, ertalab budilnik jiringlasa ham uyg'onmaydi, men uni maktabga olib borishga shoshilaman, u esa hojatxonaga shoshadi. Har kuni shunday mayda narsalar uchun uni tanqid qilaman, ikkovimizning ham kayfiyatimiz buziladi.",
    "孩子做事慢，往往是因为他们不会安排自己的时间。你应该让孩子学会管理时间。": "Bolalar ishni sekin qilishi ko'pincha vaqtini rejalay olmasligidan. Siz bolaga vaqtni boshqarishni o'rgatishingiz kerak.",
    "看来还是我的教育方法有问题。平时看她做事情慢，总想替她做，以后得让她学会安排时间，自己的事情自己做。": "Demak, tarbiya usulimda muammo bor ekan. U ishni sekin qilsa, doim o'rniga qilib qo'ygim kelardi. Endi vaqtini rejalashni va o'z ishini o'zi qilishni o'rgataman.",
}


DIALOGUE_UZ_EXTRA = {
    "你马上就要硕士毕业了吧？将来有什么打算？": "Siz yaqinda magistraturani bitirasiz, to'g'rimi? Kelajak uchun qanday rejangiz bor?",
    "我想出国读博士，一直在准备办签证需要的材料。": "Chet elga doktorantura o'qishga bormoqchiman, viza uchun kerakli hujjatlarni tayyorlab yuribman.",
    "现在材料准备得怎么样了？": "Hujjatlar hozir qanday tayyor bo'ldi?",
    "成绩证明和护照已经准备好了，另外，还跟国外的大学取得了联系，填写了报名表格。": "Baholar haqidagi ma'lumotnoma va pasport tayyor. Bundan tashqari, chet eldagi universitet bilan bog'landim va ro'yxatdan o'tish formasini to'ldirdim.",
    "还应该有国外大学给你的邀请信吧？他们把邀请信传真给你了吗？": "Yana chet el universitetidan taklifnoma bo'lishi kerak-ku? Ular taklifnomani faks orqali yubordimi?",
    "没有啊，下个星期我就要去使馆办签证了，这可怎么办？": "Yo'q-ku, keyingi hafta elchixonaga viza rasmiylashtirishga boraman, endi nima qilaman?",
    "这可是个大问题，我也不太清楚。我帮你查一下学校的电话号码，你打电话问一下吧。": "Bu jiddiy muammo ekan, men ham aniq bilmayman. Maktabning telefon raqamini topib beraman, qo'ng'iroq qilib so'rab ko'ring.",
    "谢谢您带我参观您的公司。在参观过程中我很激动，有个问题一直想问您。": "Kompaniyangizni ko'rsatganingiz uchun rahmat. Ko'rib chiqish davomida juda hayajonlandim, sizdan bir savol so'ramoqchi edim.",
    "好啊！小伙子，咱们一边吃西瓜，一边聊。": "Mayli, yigit, tarvuz yeb turib gaplashamiz.",
    "您从大学毕业开始工作，到现在才十年时间，怎么给公司赚了这么多钱？这让我非常吃惊。我想向您学习一下成功的经验。": "Universitetni bitirib ish boshlaganingizga atigi o'n yil bo'libdi, qanday qilib kompaniyaga bunchalik ko'p pul topib berdingiz? Bu meni juda hayron qoldirdi. Sizdan muvaffaqiyat tajribangizni o'rganmoqchiman.",
    "这个问题以前一个记者也问过我。做生意时虽然会遇到各种压力和困难，但是大家的机会都是相同的。你看，这里有三块大小不同的西瓜，我们用西瓜的大小代表钱的多少，要是我们一起开始吃，你会先选哪块？": "Bu savolni oldin bir muxbir ham bergan. Biznesda turli bosim va qiyinchiliklar bo'lsa ham, hammaning imkoniyati bir xil. Mana, bu yerda hajmi har xil uch bo'lak tarvuz bor. Tarvuz kattaligini pul miqdori deb olaylik. Agar bir vaqtda yeyishni boshlasak, qaysi bo'lakni birinchi tanlaysiz?",
    "我肯定先吃最大的一块了，难道您会先吃小的，放弃吃大块的机会吗？": "Men albatta eng kattasini birinchi yeyman. Nahotki siz kichigini tanlab, katta bo'lak imkoniyatidan voz kechsangiz?",
    "我会先吃最小的一块，因为在你没吃完最大的那块时，我还有时间再多吃一块，最后一定比你吃的西瓜多。听完我的回答，恐怕你已经知道我的答案了吧。": "Men eng kichigini birinchi yeyman, chunki siz eng katta bo'lakni tugatguncha men yana bir bo'lak yeyishga ulguraman, oxirida sizdan ko'proq tarvuz yeyman. Javobimni eshitib, ehtimol mening javobimni tushungandirsiz.",
    "今年放假我又回不了家了，这次我父母又要失望了。你有什么计划？": "Bu yil ta'tilda yana uyga qaytolmayman, bu safar ota-onam yana xafa bo'ladi. Sizning qanday rejangiz bor?",
    "我计划去郊区住一个月。你不是已经买好火车票了吗？你到底怎么打算的呀？": "Men shahar chetida bir oy yashashni rejalashtirdim. Siz poyezd chiptasini olib bo'lgandingiz-ku? Axir nima qilmoqchisiz?",
    "昨天一个外地的好朋友打电话说要来旅游，让我当导游，我实在不好意思拒绝。": "Kecha boshqa shahardagi yaqin do'stim qo'ng'iroq qilib, sayohatga kelishini va menga gid bo'lishni aytdi. Uni rad etishga juda uyalaman.",
    "其实拒绝并不表示不愿意帮忙。遇到解决不了的问题或者无法完成的任务时，拒绝正好说明你对朋友负责。这也是对你父母负责的态度。": "Aslida rad etish yordam berishni istamaslik degani emas. Hal qilib bo'lmaydigan muammo yoki bajarib bo'lmaydigan ishga duch kelganda rad etish do'stingiz oldidagi mas'uliyatni ko'rsatadi. Bu ota-onangiz oldidagi mas'uliyat ham.",
    "既然别人找我帮忙，说明他真的很需要我的帮助。我担心要是说“不”的话，会让他误会和伤心。": "Modomiki u mendan yordam so'ragan ekan, demak rostdan yordamim kerak. “Yo'q” desam, noto'g'ri tushunib, xafa bo'lib qolishidan xavotirdaman.",
    "别担心！如果你用一个既合适又礼貌的方法告诉朋友，他一定会原谅你的。": "Xavotir olmang! Agar do'stingizga mos va odobli usulda aytsangiz, u albatta sizni kechiradi.",
    "最近天气越来越凉快了，风一刮，草地上就会有一层厚厚的黄叶，看来秋天已经到了。": "So'nggi payt havo tobora salqinlashyapti. Shamol essa, maysazor ustida qalin sariq barglar qatlami paydo bo'ladi. Ko'rinishidan, kuz kelibdi.",
    "这几天香山特别热闹，随着气温的降低，那里许多植物的叶子都由绿变黄或者变红，吸引了很多游客参观，咱们今天也去看看吧。": "Shu kunlarda Xiangshan juda gavjum. Harorat pasaygani sari u yerdagi ko'p o'simliklarning barglari yashildan sariq yoki qizilga aylanib, ko'p sayyohlarni jalb qilyapti. Bugun biz ham borib ko'raylik.",
    "你看天上的云，今天肯定雨大。再说，香山上看红叶的人太多了。咱们改天去长城吧，广播里说那里也有不少专门看红叶的好地方。": "Osmondagi bulutlarga qarang, bugun yomg'ir kuchli bo'lsa kerak. Ustiga-ustak Xiangshanda qizil barg ko'radigan odam juda ko'p. Boshqa kuni Buyuk devorga boraylik, radioda u yerda ham qizil barg tomosha qilish uchun maxsus joylar ko'p deyishdi.",
    "真可惜，我还想多照点儿香山的照片呢。去长城倒是一个好主意，那我们明天去吧。": "Afsus, Xiangshanda ko'proq suratga olmoqchi edim. Buyuk devorga borish ham yaxshi fikr-ku, unda ertaga boraylik.",
    "明天恐怕也不行，明天是我爸的生日。": "Ertaga ham bo'lmasa kerak, ertaga dadamning tug'ilgan kuni.",
    "没关系，那我们再约时间。": "Mayli, unda boshqa vaqt kelishamiz.",
    "你的这只大黑狗毛真漂亮，而且这么聪明，每次见了都想抱一抱它。": "Bu katta qora itingizning juni juda chiroyli, o'zi ham aqlli ekan. Har safar ko'rsam quchoqlagim keladi.",
    "狗是很聪明的动物，只要稍微花点儿时间教教它，它就能学会很多东西。": "It juda aqlli hayvon. Unga ozgina vaqt ajratib o'rgatsangiz, ko'p narsani o'rganadi.",
    "听你这么一说，我现在也想养一只狗了。每次你让它干什么，它就像能听懂你的话一样去做。你教它是不是用了什么特别的方法？": "Gapingizni eshitib, men ham it boqgim kelib qoldi. Har safar biror narsa buyursangiz, gapingizni tushungandek bajaradi. Uni o'rgatishda maxsus usul ishlatdingizmi?",
    "要让它完成一些任务，只教一次是不够的，应该耐心地一遍一遍地教给它，使它熟悉，然后它就会严格按照你的要求做了。": "Uni ayrim vazifalarni bajarishga o'rgatish uchun bir marta o'rgatish yetmaydi. Sabr bilan qayta-qayta o'rgatib, odatlantirish kerak, keyin u sizning talabingizga qat'iy amal qiladi.",
    "看来没有想的那么容易。": "Ko'rinishidan, o'ylaganimdek oson emas ekan.",
    "狗是我们的好朋友，它能听懂人的话，明白人的心情。在你心里难受的时候，它会一直陪着你。": "It bizning yaxshi do'stimiz. U odamning gapini tushunadi, kayfiyatini sezadi. Ko'nglingiz g'amgin bo'lganda yoningizda bo'ladi.",
    "上个月我去了趟北京动物园，那里约有500种动物，听导游说北京动物园是亚洲最大的动物园之一。": "O'tgan oy Pekin hayvonot bog'iga bir borib keldim. U yerda taxminan 500 xil hayvon bor ekan. Gidning aytishicha, Pekin hayvonot bog'i Osiyodagi eng katta hayvonot bog'laridan biri.",
    "去年放暑假的时候，我也去过一次，我在那儿看了马、熊猫、老虎等动物。我特别喜欢熊猫，可惜它们当时大都在睡觉。": "O'tgan yili yozgi ta'tilda men ham bir marta borganman. U yerda ot, panda, yo'lbars kabi hayvonlarni ko'rdim. Pandalarni ayniqsa yaxshi ko'raman, afsuski o'shanda ularning aksari uxlayotgandi.",
    "我去的那天正赶上六一儿童节，许多父母带着孩子去动物园。入口处排队的人很多，动物园里热闹极了。大熊猫们也变得特别活泼，我还给它们照了不少照片呢。": "Men borgan kun aynan 1-iyun Bolalar kuniga to'g'ri kelibdi, ko'p ota-onalar bolalarini hayvonot bog'iga olib kelishgan. Kirish joyida navbat juda katta, bog' esa nihoyatda gavjum edi. Pandalar ham juda sho'x bo'lib qolgan, ularning ko'p suratini oldim.",
    "大熊猫身子胖胖的，样子可爱极了。": "Pandalar gavdasi dumaloq, ko'rinishi juda yoqimtoy.",
    "不过，它们数量不多，现在全世界一共才有一千多只吧。": "Lekin ularning soni ko'p emas, hozir butun dunyoda jami mingdan sal ko'proq bo'lsa kerak.",
    "以前只有中国有大熊猫，为了表示友好，从1957年开始，中国把大熊猫作为礼物送给其他一些国家。现在，很多国家的人们在本国都能看到大熊猫了。": "Avvallari panda faqat Xitoyda bo'lgan. Do'stlikni ifodalash uchun 1957 yildan boshlab Xitoy pandalarni sovg'a sifatida ayrim mamlakatlarga yuborgan. Hozir ko'p mamlakat odamlari pandani o'z davlatida ham ko'ra oladi.",
    "上次女儿问我飞机是怎么起飞和降落的，真不知道该怎么回答她，她现在总是有各种各样的“为什么”。": "O'tgan safar qizim mendan samolyot qanday uchib, qanday qo'nishini so'radi, unga qanday javob berishni bilmadim. Hozir u doim turli-tuman “nega”larni so'raydi.",
    "孩子眼中的世界是美丽和奇特的。有一本书叫《新十万个为什么》，现在卖得非常火。书里的内容都是儿童想知道的科学知识，相信你女儿一定喜欢读。": "Bolalar ko'zidagi dunyo chiroyli va g'aroyib. 《Yangi yuz mingta nega》 degan kitob bor, hozir juda mashhur. Ichidagi mavzular bolalar bilmoqchi bo'lgan ilmiy bilimlar, qizingiz albatta yoqtiradi.",
    "难道它和我们小时候看的《十万个为什么》不一样吗？作者是谁啊？": "Nahotki u biz bolaligimizda o'qigan 《Yuz mingta nega》dan boshqacha bo'lsa? Muallifi kim?",
    "作者的名字我没记住。《新十万个为什么》的内容更新，介绍了各种科学知识，包括地球、动物、植物、交通、科学技术、社会和文化等很多方面。": "Muallifning ismini eslab qolmadim. 《Yangi yuz mingta nega》 mazmuni yangiroq, turli ilmiy bilimlarni tanishtiradi: Yer, hayvonlar, o'simliklar, transport, texnologiya, jamiyat va madaniyat kabi ko'p yo'nalishlar.",
    "太好了！不过她这么小，我不知道她是否能读懂。": "Juda yaxshi! Lekin u hali kichkina, o'qib tushuna oladimi yo'qmi bilmayman.",
    "放心吧，这本书的语言简单易懂，一定能增长孩子的科学知识。": "Xavotir olmang, bu kitobning tili sodda va tushunarli, bolangizning ilmiy bilimini albatta oshiradi.",
    "现在的大学生一遇到不明白的问题，可以马上在网上查找答案，几秒钟就把问题解决了，这比我们上学的时候方便多了。": "Hozirgi talabalar tushunmagan savolga duch kelsa, darhol internetdan javob topa oladi, bir necha soniyada muammo hal bo'ladi. Bu biz o'qigan davrdagidan ancha qulay.",
    "现在的人们，尤其是大学生开始普遍使用电脑，他们的生活已经离不开电脑。据调查，70%的人遇到问题时，首先想到的就是上网找答案。": "Hozir odamlar, ayniqsa talabalar kompyuterdan keng foydalanadi, ularning hayoti kompyutersiz bo'lmay qoldi. So'rovga ko'ra, odamlarning 70 foizi muammoga duch kelsa, birinchi bo'lib internetdan javob qidirishni o'ylaydi.",
    "电脑和互联网技术的发展使学生们的学习方式发生了很多变化，不过天天对着电脑看，眼睛实在受不了。": "Kompyuter va internet texnologiyalari rivoji talabalarning o'qish usulini juda o'zgartirdi, lekin har kuni kompyuterga qarab o'tirishga ko'z chiday olmaydi.",
    "不仅是学习方式，而且连生活方式也发生了很大改变。现在越来越多的学生喜欢在网上写日记，他们说这样可以让朋友及时了解自己的生活。": "Faqat o'qish usuli emas, hatto yashash tarzi ham katta o'zgardi. Hozir tobora ko'p talaba internetda kundalik yozishni yoqtiradi, ular shunda do'stlari hayotidan vaqtida xabardor bo'ladi deyishadi.",
    "这个办法不错，既能方便大家的交流，还能节约用纸，保护环境。但是如果别人都能看到我的日记的话，多不安全啊！": "Bu usul yomon emas: ham muloqotni qulay qiladi, ham qog'ozni tejab, atrof-muhitni himoya qiladi. Lekin kundaligimni hamma ko'rsa, juda xavfli-ku!",
    "放心吧，可以给网上的日记加密码，那样只有得到了允许，别人才能看到。": "Xavotir olmang, internetdagi kundalikka parol qo'yish mumkin. Shunda faqat ruxsat olgan odamlar ko'ra oladi.",
    "我昨天晚上做了一个特别奇怪的梦，梦到自己正在一座桥上走，走着走着，突然开过来一辆车，非常危险，接着又梦见我跳到车上，跟警察一起抓住了一个坏人。": "Kecha tunda juda g'alati tush ko'rdim: ko'prik ustida yurayotgan emishman, yurib ketayotib birdan bir mashina kelib qoldi, juda xavfli edi. Keyin tushimda mashinaga sakrab chiqib, politsiya bilan birga yomon odamni ushladim.",
    "奇怪，你怎么总能记住自己做了什么梦？我好像从来没做过梦。": "Qiziq, siz qanday qilib har doim tushlaringizni eslab qolasiz? Men go'yo hech qachon tush ko'rmayman.",
    "每个人都会做梦，区别只是有多有少。有的人睡醒之后还记得梦里的事情，有的人却记不清楚了。你之所以觉得从来没做过梦，只不过是忘记了。": "Har bir odam tush ko'radi, farqi faqat ko'p yoki kamligida. Ba'zilar uyg'ongach tushdagi voqealarni eslaydi, ba'zilar esa aniq eslay olmaydi. Siz hech tush ko'rmayman deb o'ylashingiz shunchaki uni unutganingiz uchun.",
    "你说的有道理，我一般都是一觉睡到天亮。很多人认为做梦是上天要告诉他们将来会发生的一些事情，可能上天不想让我知道吧。": "Gapingizda jon bor. Men odatda tonggacha uyg'onmay uxlayman. Ko'p odam tushni osmon ularga kelajakda bo'ladigan narsalarni aytmoqda deb o'ylaydi. Balki osmon menga bilishni istamagandir.",
    "一般晚上睡觉时，身体感觉到什么，人就容易梦到什么内容。记得有一次，我晚饭吃得太咸，那天晚上就梦见自己到处找商店买矿泉水。": "Odatda kechasi uxlaganda tana nimani his qilsa, odam shunga oid tush ko'rishi oson. Bir safar kechki ovqatni juda sho'r yegandim, o'sha kecha hamma joydan do'kon qidirib, mineral suv olmoqchi bo'lganimni tush ko'rganman.",
    "很多人都试着对梦进行解释，有些人甚至专门写过这方面的书，可惜到现在仍然没有一个科学的说法。": "Ko'p odamlar tushni tushuntirishga urinadi, ba'zilar hatto shu mavzuda maxsus kitob ham yozgan. Afsuski, hozirgacha ilmiy izoh yo'q.",
    "老师，您好！我希望下个学期在这里继续学习，请问还需要重新申请吗？": "Ustoz, salom! Keyingi semestr ham shu yerda o'qishni davom ettirmoqchiman, qayta ariza topshirishim kerakmi?",
    "是的。给你表格，出生年月、性别、护照号码都要填，还有联系地址、联系电话。": "Ha. Mana sizga forma, tug'ilgan yilingiz va oyingiz, jinsingiz, pasport raqamingizni to'ldiring. Aloqa manzili va telefon raqami ham kerak.",
    "真抱歉，我不小心把护照号码填错了，您能再给我一份新的申请表吗？": "Kechirasiz, ehtiyotsizlik bilan pasport raqamini xato yozibman, menga yana bitta yangi ariza formasi bera olasizmi?",
    "没关系，不用道歉，谁都有粗心填错的时候。申请表都被别人拿走了，我给你重新打印一份，你等一下。": "Mayli, kechirim so'rash shart emas, hamma ham beparvolik qilib xato to'ldirishi mumkin. Ariza formalari boshqalar tomonidan olib ketildi, sizga qayta chiqarib beraman, bir oz kuting.",
    "（高老师打印，马克填表。）": "(Gao o'qituvchi chiqaradi, Mark formani to'ldiradi.)",
    "这次我按照要求都填写完了，请问还需要做别的事情吗？": "Bu safar hammasini talab bo'yicha to'ldirdim. Yana boshqa ish qilishim kerakmi?",
    "请把你的护照给我，我们要把护照复印一下。": "Pasportingizni menga bering, biz pasportdan nusxa olishimiz kerak.",
    "呀，你的手怎么流血了？等一下，我给你包起来。": "Voy, qo'lingiz nega qonayapti? Bir oz kuting, bog'lab qo'yaman.",
    "没关系，我想给你做点儿羊肉饺子，刚才用刀切肉的时候把手弄破了。": "Hechqisi yo'q, sizga qo'y go'shtli jiaozi qilmoqchi edim, hozirgina go'shtni pichoq bilan kesayotganda qo'limni kesib oldim.",
    "你也太不小心了，不过好像不太严重，过几天就好了。衣服上也有一点儿血，你把衣服脱下来，我给你洗洗。": "Juda ehtiyotsiz bo'libsiz, lekin unchalik jiddiyga o'xshamaydi, bir necha kunda tuzaladi. Kiyimingizga ham ozroq qon tegibdi, kiyimni yeching, yuvib beraman.",
    "看来今天吃不上羊肉饺子了。": "Ko'rinishidan, bugun qo'y go'shtli jiaozi yeyolmaymiz.",
    "那我们就吃点儿别的。我常去的那家理发店附近有个餐厅，那里的包子很好吃，我一会儿去买一点儿。": "Unda boshqa narsa yeymiz. Men tez-tez boradigan sartaroshxona yonida bir restoran bor, u yerning baozisi juda mazali. Hozir borib ozroq olib kelaman.",
    "好吧，我衣服口袋里有十几块零钱，买包子应该够。": "Mayli, kiyimim cho'ntagida o'n necha yuan mayda pul bor, baozi olishga yetishi kerak.",
    "我早上跟你打招呼，你没看见。想不到又在这儿碰见你了。": "Ertalab sizga salom bergandim, ko'rmadingiz. Yana shu yerda uchrashib qolamiz deb o'ylamagandim.",
    "真是对不起，我不是故意的，今天早上我忘戴眼镜了，看不清楚。": "Rostdan kechirasiz, ataylab qilmadim. Bugun ertalab ko'zoynagimni taqishni unutibman, yaxshi ko'ra olmadim.",
    "刚才我在旁边看到你跳中国舞了，没看出来你跳得这么好！难道你以前在你们国家就学过中国舞蹈吗？": "Hozirgina yon tomondan xitoycha raqs tushayotganingizni ko'rdim. Bunchalik yaxshi raqs tushishingizni bilmasdim! Nahotki avval o'z davlatingizda xitoy raqsini o'rgangan bo'lsangiz?",
    "我小时候妈妈教我跳过两年的舞，所以稍微有点儿基础。再说，舞蹈不仅是一门艺术，也是一种“语言”，这种语言与国籍无关，无论哪个国家的人都能看懂。": "Bolaligimda onam menga ikki yil raqs o'rgatgan, shuning uchun ozroq asosim bor. Bundan tashqari, raqs nafaqat san'at, balki bir turdagi “til” ham. Bu til millatga bog'liq emas, qaysi davlat odami bo'lishidan qat'i nazar tushuna oladi.",
    "太好了！我刚学习跳这种舞没多久，你帮我看看，我的这个动作对不对。": "Juda yaxshi! Men bu raqsni yaqinda o'rgana boshladim, mana bu harakatim to'g'rimi, ko'rib bera olasizmi?",
    "你这个动作做得还是不太标准，我给你跳一遍。你仔细看着，应该像我这样：先抬胳膊，然后抬腿，最后头再向右转一下。": "Bu harakatingiz hali unchalik standart emas. Men bir marta ko'rsataman, diqqat bilan qarang: avval qo'lni ko'tarasiz, keyin oyoqni ko'tarasiz, oxirida boshni o'ngga burasiz.",
    "该加油了，去机场的路上有加油站吗？": "Yoqilg'i quyish kerak bo'ldi, aeroport yo'lida yoqilg'i shoxobchasi bormi?",
    "我记得过了长江大桥往右一拐就有一个，大概有四五公里远。": "Esimda, Changjiang ko'prigidan o'tib o'ngga burilsak bittasi bor, taxminan 4-5 kilometr uzoqda.",
    "好，那我就放心了，别开着开着没油了。你去北京的航班是几点的？时间来得及吗？": "Yaxshi, unda xotirjam bo'ldim. Yo'lda ketayotib yoqilg'i tugab qolmasin. Pekinga reysingiz soat nechada? Ulguramizmi?",
    "航班本来是10点的，后来机场网站上通知推迟了一个小时，所以9点半以前到就应该没问题。": "Reys aslida 10 da edi, keyin aeroport saytida bir soatga kechiktirilgani haqida xabar berildi, shuning uchun 9:30 gacha borsak muammo bo'lmasa kerak.",
    "刚才我还有点儿担心来不及呢。一会儿加完油，往西走五百米就能上高速公路。走高速公路大约半个小时就到了。": "Hozirgina ulgurmay qolamizmi deb biroz xavotirlangandim. Keyin yoqilg'i quyib, g'arbga 500 metr yursak avtomagistralga chiqamiz. Avtomagistralda taxminan yarim soatda yetamiz.",
    "一会儿我自己进去换登机牌，你就不用送我了，等我到了首都机场再给你发短信。": "Keyin o'zim ichkariga kirib, boarding pass olaman, meni kuzatib qo'yishingiz shart emas. Poytaxt aeroportiga yetganimda SMS yuboraman.",
    "女儿下个星期就要放寒假了，到时候咱们带她去旅游，放松放松，怎么样？": "Qizimiz keyingi hafta qishki ta'tilga chiqadi, o'shanda uni sayohatga olib borib, biroz dam oldirsak qanday?",
    "平时女儿那么多课，总是说想去旅行，但是没时间，怪可怜的。这次放假咱们带她去哪儿玩儿比较好呢？": "Odatda qizimizning darsi juda ko'p, doim sayohatga borgisi keladi, lekin vaqti yo'q, bechora. Bu ta'tilda uni qayerga olib borgan yaxshi?",
    "去年我同事带她儿子去广西玩儿了一趟，听说很不错，我们就去广西吧。": "O'tgan yili hamkasbim o'g'lini Guangxiga olib borib kelgan, eshitishimcha juda yaxshi ekan. Guangxiga boraylik.",
    "好啊，那里的气候和北方很不同，即使是冬天，也非常暖和，还能吃到许多新鲜的水果。等女儿一回来我就告诉她这个好消息。": "Mayli, u yerning iqlimi shimoldan juda farq qiladi, hatto qishda ham juda iliq, ko'p yangi meva yeyish mumkin. Qizimiz qaytishi bilan bu yaxshi xabarni aytaman.",
    "先别着急说。中午我们不是要去对面的饭店吃烤鸭，祝贺她考试成绩都合格吗？那时候再告诉她，不是更好？": "Hozir aytishga shoshilmang. Tushda ro'paradagi restoranga qovurilgan o'rdak yeyib, imtihonlari hammasidan o'tganini tabriklashga boramiz-ku? O'shanda aytsak yaxshiroq emasmi?",
    "好主意，到时她知道了肯定特别开心。": "Yaxshi fikr, o'shanda bilsa juda xursand bo'ladi.",
    "这么多照片，都是你这次去丽江旅行时照的？那里的自然风景可真美！": "Buncha ko'p suratning hammasini shu safar Lijiangga borganda olganmisiz? U yerning tabiiy manzarasi juda chiroyli ekan!",
    "是啊，小城四季的风景都很美，而且环境保护得也很好，因此每年都吸引着成千上万的游客去那儿旅游。": "Ha, bu kichik shaharning to'rt fasldagi manzarasi ham chiroyli, atrof-muhiti ham yaxshi himoya qilingan. Shuning uchun har yili minglab sayyohlarni jalb qiladi.",
    "这张照片上和你干杯的那个人是少数民族吗？她打扮得真漂亮。": "Bu suratda siz bilan qadah ko'tarayotgan odam ozchilik millat vakilimi? Juda chiroyli kiyinibdi.",
    "她是我们的导游，不是少数民族。一路上她给我们讲了很多有趣的笑话。有一次我把存包的钥匙丢了，最后还是她帮我找到的。这张照片就是找到钥匙后，我们一起照的。": "U bizning gidimiz, ozchilik millat vakili emas. Yo'lda bizga juda ko'p qiziqarli hazillar aytib berdi. Bir safar sumka saqlash joyining kalitini yo'qotib qo'ydim, oxirida uni o'sha topib berdi. Bu surat kalit topilgandan keyin birga tushgan suratimiz.",
    "明年我有机会也去那儿看看，到时把你的导游介绍给我吧。究竟哪个季节去丽江旅游比较好呢？": "Kelasi yil imkon bo'lsa men ham u yerga borib ko'raman, o'shanda gidingizni menga tanishtirib qo'ying. Lijiangga qaysi faslda borgan yaxshiroq?",
    "那儿最美的季节是春天和秋天，不过那时候人比较多。稍微好一点儿的时间是每年12月到第二年3月。这段时间去丽江的话，无论交通还是吃、住都很便宜。": "U yerning eng chiroyli fasllari bahor va kuz, lekin o'sha paytda odam ko'p bo'ladi. Biroz qulayroq vaqt har yil dekabrdan keyingi yil martgacha. Shu davrda Lijiangga borsangiz, transport ham, ovqat va turar joy ham arzon bo'ladi.",
}

DIALOGUE_UZ.update(DIALOGUE_UZ_EXTRA)


POS_PREFIXES = (
    "proper noun",
    "conj.",
    "prep.",
    "pron.",
    "part.",
    "aux.",
    "adj.",
    "adv.",
    "n.",
    "v.",
    "m.",
)


def _split_pos(meaning: str) -> str:
    for prefix in POS_PREFIXES:
        if meaning.startswith(prefix):
            return prefix
    return ""


def _localized_title(title: str) -> str:
    return json.dumps({"uz": title, "ru": title, "tj": title}, ensure_ascii=False)


def _vocabulary_json(vocab: list[tuple[str, str, str]]) -> str:
    return json.dumps(
        [
            {
                "no": index,
                "zh": zh,
                "pinyin": pinyin,
                "pos": _split_pos(meaning),
                "uz": VOCAB_UZ.get(zh, ""),
            }
            for index, (zh, pinyin, meaning) in enumerate(vocab, 1)
        ],
        ensure_ascii=False,
    )


def _dialogue_json(dialogues: list[tuple[str, str, list[tuple[str, str]]]]) -> str:
    return json.dumps(
        [
            {
                "block_no": block_no,
                "section_label": section_label,
                "scene_label_zh": scene_label,
                "scene_uz": SCENE_UZ.get(scene_label, scene_label),
                "dialogue": [
                    {
                        "speaker": speaker,
                        "zh": text,
                        "pinyin": "",
                        "uz": DIALOGUE_UZ.get(text, ""),
                    }
                    for speaker, text in lines
                ],
                "grammar_notes": [],
            }
            for block_no, (section_label, scene_label, lines) in enumerate(dialogues, 1)
        ],
        ensure_ascii=False,
    )


def _flatten_dialogue_lines(
    dialogues: list[tuple[str, str, list[tuple[str, str]]]]
) -> list[str]:
    return [
        text
        for _, _, lines in dialogues
        for _, text in lines
        if text and not text.startswith("（")
    ]


def _exercise_json(order: int) -> str:
    data = LESSON_DATA[order]
    vocab = data["vocab"]
    dialogue_lines = _flatten_dialogue_lines(data["dialogues"])

    zh_items = [
        {
            "prompt_uz": VOCAB_UZ.get(zh, zh),
            "prompt_ru": VOCAB_UZ.get(zh, zh),
            "prompt_tj": VOCAB_UZ.get(zh, zh),
            "answer": zh,
            "pinyin": pinyin,
        }
        for zh, pinyin, _ in vocab[:5]
    ]
    uz_items = [
        {
            "prompt_uz": zh,
            "prompt_ru": zh,
            "prompt_tj": zh,
            "answer": VOCAB_UZ.get(zh, ""),
            "pinyin": pinyin,
        }
        for zh, pinyin, _ in vocab[5:10]
    ]

    blank_items = []
    used_words = set()
    used_sentences = set()
    for zh, pinyin, _ in vocab:
        if zh in used_words:
            continue
        for sentence in dialogue_lines:
            if sentence in used_sentences:
                continue
            if zh in sentence:
                blank_items.append(
                    {
                        "prompt_uz": sentence.replace(zh, "______", 1),
                        "prompt_ru": sentence.replace(zh, "______", 1),
                        "prompt_tj": sentence.replace(zh, "______", 1),
                        "answer": zh,
                        "pinyin": pinyin,
                    }
                )
                used_words.add(zh)
                used_sentences.add(sentence)
                break
        if len(blank_items) >= 4:
            break

    exercises = [
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction_uz": "Quyidagi ma'nolarning xitoychasini yozing:",
            "instruction_ru": "Напишите китайский вариант следующих значений:",
            "instruction_tj": "Варианти хитоии маъноҳои зеринро нависед:",
            "items": zh_items,
        },
        {
            "no": 2,
            "type": "translate_to_uzbek",
            "instruction_uz": "Quyidagi so'zlarning o'zbekcha ma'nosini yozing:",
            "instruction_ru": "Напишите узбекское значение следующих слов:",
            "instruction_tj": "Маънои ӯзбекии калимаҳои зеринро нависед:",
            "items": uz_items,
        },
    ]
    if blank_items:
        exercises.append(
            {
                "no": 3,
                "type": "fill_blank",
                "instruction_uz": "Kitob dialoglaridan olingan gaplarda bo'sh joyni to'ldiring:",
                "instruction_ru": "Заполните пропуски в предложениях из диалогов учебника:",
                "instruction_tj": "Ҷойҳои холиро дар ҷумлаҳои муколамаҳои китоб пур кунед:",
                "items": blank_items,
            }
        )
    return json.dumps(exercises, ensure_ascii=False)


def _answers_json(order: int) -> str:
    exercises = json.loads(_exercise_json(order))
    return json.dumps(
        [
            {
                "no": exercise["no"],
                "answers": [
                    item.get("answer", "")
                    for item in exercise.get("items", [])
                    if item.get("answer")
                ],
            }
            for exercise in exercises
        ],
        ensure_ascii=False,
    )


def _grammar_json(order: int) -> str:
    data = LESSON_DATA[order]
    dialogue_lines = _flatten_dialogue_lines(data["dialogues"])
    grammar = []
    for index, title in enumerate(GRAMMAR_TITLES.get(order, []), 1):
        key = (
            title.replace("……", "")
            .replace("V", "")
            .replace("着", "着")
            .replace("疑问代词活用表示任指", "")
        )
        examples = []
        for sentence in dialogue_lines:
            if key and key in sentence:
                examples.append({"zh": sentence, "pinyin": "", "uz": DIALOGUE_UZ.get(sentence, "")})
            if len(examples) >= 2:
                break
        grammar.append(
            {
                "no": index,
                "title_zh": title,
                "title_uz": title,
                "rule_uz": "Kitobdagi grammatika nuqtasi. Dars dialoglaridagi qo'llanishini qayta o'qing.",
                "examples": examples,
            }
        )
    return json.dumps(grammar, ensure_ascii=False)


def _homework_json(order: int) -> str:
    data = LESSON_DATA[order]
    title = data["title"]
    words = [zh for zh, _, _ in data["vocab"][:8]]
    scene = data["dialogues"][0][1] if data["dialogues"] else title
    return json.dumps(
        [
            {
                "no": 1,
                "instruction_uz": "Quyidagi dars so'zlaridan foydalanib 5 ta xitoycha gap tuzing:",
                "instruction_ru": "Составьте 5 китайских предложений со словами урока:",
                "instruction_tj": "Бо калимаҳои дарс 5 ҷумлаи хитоӣ тартиб диҳед:",
                "words": words,
                "example": f"{words[0]} / {words[1]} / {words[2]}",
            },
            {
                "no": 2,
                "instruction_uz": "Kitobdagi dialoglardan bittasini tanlab, mazmunini 4-5 gap bilan o'zbekcha yozing.",
                "instruction_ru": "Выберите один диалог из учебника и кратко перескажите его по-узбекски в 4-5 предложениях.",
                "instruction_tj": "Яке аз муколамаҳои китобро интихоб карда, мазмунашро бо 4-5 ҷумла ба ӯзбекӣ нависед.",
                "topic_uz": scene,
                "topic_ru": scene,
                "topic_tj": scene,
            },
            {
                "no": 3,
                "instruction_uz": "Dars mavzusida qisqa dialog yozing. Kamida 6 ta yangi so'z ishlating.",
                "instruction_ru": "Напишите короткий диалог по теме урока. Используйте минимум 6 новых слов.",
                "instruction_tj": "Дар мавзӯи дарс муколамаи кӯтоҳ нависед. Камаш 6 калимаи навро истифода баред.",
                "topic_uz": title,
                "topic_ru": title,
                "topic_tj": title,
            },
        ],
        ensure_ascii=False,
    )


def _review_json(order: int) -> str:
    data = LESSON_DATA[order]
    return json.dumps(
        [
            {
                "title_uz": f"Dars {order}: {data['title']}",
                "vocabulary": [
                    {"zh": zh, "pinyin": pinyin, "uz": VOCAB_UZ.get(zh, "")}
                    for zh, pinyin, _ in data["vocab"][:10]
                ],
                "dialogues": [
                    {
                        "section_label": section_label,
                        "scene_uz": SCENE_UZ.get(scene_label, scene_label),
                    }
                    for section_label, scene_label, _ in data["dialogues"]
                ],
                "grammar": GRAMMAR_TITLES.get(order, []),
            }
        ],
        ensure_ascii=False,
    )


def build_lesson(order: int) -> dict:
    data = LESSON_DATA[order]
    title = data["title"]
    return {
        "level": "hsk4",
        "lesson_order": order,
        "lesson_code": f"HSK4-L{order:02d}",
        "title": title,
        "goal": _localized_title(title),
        "intro_text": _localized_title(title),
        "vocabulary_json": _vocabulary_json(data["vocab"]),
        "dialogue_json": _dialogue_json(data["dialogues"]),
        "grammar_json": _grammar_json(order),
        "exercise_json": _exercise_json(order),
        "answers_json": _answers_json(order),
        "homework_json": _homework_json(order),
        "review_json": _review_json(order),
        "is_active": True,
    }


async def upsert_hsk4_lesson(order: int) -> None:
    lesson = build_lesson(order)
    async with SessionLocal() as session:
        result = await session.execute(
            select(CourseLesson).where(CourseLesson.lesson_code == lesson["lesson_code"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            for key, value in lesson.items():
                setattr(existing, key, value)
            print(f"updated: {lesson['lesson_code']}")
        else:
            session.add(CourseLesson(**lesson))
            print(f"inserted: {lesson['lesson_code']}")

        await session.commit()


def run_upsert(order: int):
    async def _upsert_lesson():
        await upsert_hsk4_lesson(order)

    return _upsert_lesson


if __name__ == "__main__":
    for lesson_order in range(12, 21):
        asyncio.run(upsert_hsk4_lesson(lesson_order))
