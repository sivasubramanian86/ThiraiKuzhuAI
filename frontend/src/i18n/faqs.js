/**
 * Localized FAQ Items across World & Indian Cinema Languages.
 */
export const LOCALIZED_FAQS = {
  en: [
    {
      category: 'Architecture & Personas',
      question: 'What is Thirai Kuzhu AI (திரை குழு AI)?',
      answer: 'Thirai Kuzhu AI is an autonomous, multi-agent film production operating system and incident command center designed for Indian and global cinema. It models the entire production hierarchy across 17 specialized studio departments (369 personas), automating triage, continuity, safety, multimodal asset review, and real-time observability.'
    },
    {
      category: 'Architecture & Personas',
      question: 'How are the 369 personas structured across the 17 Bands?',
      answer: 'Personas are organized into 17 Department Bands (A: Executive, B: Direction, C: Screenplay, D: Casting, E: Cinematography, F: Production Design, G: Costume/HMU, H: Sound, I: Stunts, J: VFX, K: Editorial, L: Music, M: DI/Color, N: Distribution, O: Legal/Censor, P: Marketing, Q: Virtual Production), plus Cross-Band Composites (COMP01..08) and Red-Team Antagonists (ANTG01..05).'
    },
    {
      category: 'Governance & Authority',
      question: 'What is the strict difference between can_block: true and can_block: false?',
      answer: 'Personas with can_block: true (such as B01 Director, I01 Stunt Director, O01 Legal Counsel) possess executive veto power to immediately halt sequences or shooting when safety, copyright, or continuity violations occur. In contrast, personas with can_block: false (and all dynamically spawned SMEs under Section 19) operate strictly in an advisory and consultative capacity.'
    },
    {
      category: 'Dynamic SMEs',
      question: 'How does Section 19 contract dynamic SME synthesis work?',
      answer: 'When a screenplay scene demands specialized domain verification (e.g. Chola bronze metallurgy, orbital astrodynamics, microtonal ragas), the Dynamic SME Studio extracts entities, selects a parent persona, and instantiates an ephemeral specialist with read-only tools and a guaranteed can_block: false contract.'
    },
    {
      category: 'Debate & Arbitration',
      question: 'How does the Dialectical Arbitration Debate engine resolve creative deadlocks?',
      answer: 'When two department heads hold opposing positions (e.g., Cinematographer requesting 8K 120fps IMAX vs Line Producer enforcing memory and budget limits), the system initiates a structured multi-round debate arbitrated by an executive persona (e.g., A01 Producer or B01 Director) to yield a binding, continuity-preserving compromise.'
    },
    {
      category: 'Adversarial Testing',
      question: 'What do the 5 Red-Team Antagonists simulate?',
      answer: 'The red-team agents stress-test production plans before shooting begins: ANTG01 breaks schedules with talent date collisions; ANTG02 injects copyright and plagiarism claims; ANTG03 exposes narrative pacing holes and cliches; ANTG04 probes dailies for piracy leaks; and ANTG05 simulates monsoons and force majeure events.'
    },
    {
      category: 'Multimodal Media',
      question: 'How does the MultiModal Media Studio inspect film assets?',
      answer: 'Powered by Gemini 2.5 and 3.8 Flash multimodal reasoning, it processes four distinct modalities: Screenplay call sheet scans (OCR/Vision), Storyboard concept stills (Framing/Color/Aspect Ratio), Foley and dialogue WAVs (Dolby Atmos spatial bed/frequency transients), and Video dailies (HFR frame drop/wire paint-out detection).'
    },
    {
      category: 'Observability',
      question: 'How does Grafana Cloud MCP Streamable HTTP transport function?',
      answer: 'Thirai Kuzhu AI streams real-time telemetry into Grafana Cloud using the Model Context Protocol (MCP) Streamable HTTP transport. It tracks Prometheus metrics (CDN 504 errors, CUDA VRAM, Atmos drift), correlates Tempo traces, and auto-injects director mitigation annotations directly onto Grafana production dashboards.'
    }
  ],
  ta: [
    {
      category: 'கட்டமைப்பு & பாத்திரங்கள்',
      question: 'திரை குழு AI (Thirai Kuzhu AI) என்றால் என்ன?',
      answer: 'திரை குழு AI என்பது இந்திய மற்றும் உலக சினிமா தயாரிப்புகளுக்கான ஒரு தன்னாட்சி மல்டி-ஏஜென்ட் ஆப்பரேட்டிங் சிஸ்டம் மற்றும் கட்டுப்பாட்டு மையம். இது 17 சிறப்பு ஸ்டுடியோ துறைகளில் (369 பாத்திரங்கள்) தயாரிப்பு படிநிலையை மாதிரியாக கொண்டு, நிகழ்நேர கிரஃபானா க்ளவுட் கண்காணிப்புடன் இயங்குகிறது.'
    },
    {
      category: 'கட்டமைப்பு & பாத்திரங்கள்',
      question: '17 பிரிவுகளில் 369 பாத்திரங்கள் எவ்வாறு கட்டமைக்கப்பட்டுள்ளன?',
      answer: 'பாத்திரங்கள் 17 துறைப் பிரிவுகளாக பிரிக்கப்பட்டுள்ளன (A: நிர்வாகம், B: இயக்கம், C: திரைக்கதை, D: நடிகர்கள் தேர்வு, E: ஒளிப்பதிவு, F: தயாரிப்பு வடிவமைப்பு, G: ஆடை/ஒப்பனை, H: ஒலி, I: சண்டைப்பயிற்சி, J: VFX, K: படத்தொகுப்பு, L: இசை, M: கலரிங், N: விநியோகம், O: சட்டம், P: விளம்பரம், Q: மெய்நிகர் தயாரிப்பு), மேலும் கூட்டுப் பாத்திரங்கள் (COMP) மற்றும் 5 எதிரணி முகவர்கள் (ANTG).'
    },
    {
      category: 'நிர்வாகம் & அதிகாரம்',
      question: 'can_block: true மற்றும் can_block: false இடையே உள்ள கடுமையான வேறுபாடு என்ன?',
      answer: 'can_block: true கொண்ட பாத்திரங்கள் (இயக்குனர் B01, சண்டை இயக்குனர் I01, சட்ட ஆலோசகர் O01) பாதுகாப்பு, பதிப்புரிமை அல்லது தொடர்ச்சி மீறல்கள் ஏற்படும் போது காட்சிகளை உடனடியாக நிறுத்தும் வீட்டோ அதிகாரம் கொண்டவை. can_block: false கொண்டவர்கள் ஆலோசனை மட்டுமே வழங்குவர்.'
    },
    {
      category: 'சிறப்பு நிபுணர்கள் (SME)',
      question: 'பிரிவு 19 ஒப்பந்தத்தின் கீழ் நிபுணர் உருவாக்கம் எவ்வாறு செயல்படுகிறது?',
      answer: 'திரைக்கதை காட்சியில் சிறப்பு கள சரிபார்ப்பு தேவைப்படும் போது (எ.கா. சோழர் கால வெண்கல வார்ப்படம், விண்வெளி இயக்கவியல், மைக்ரோடோனல் ராகங்கள்), பிரிவு 19 கீழ் can_block: false விதியுடன் தற்காலிக ஆலோசகர்கள் உருவாக்கப்படுகின்றனர்.'
    },
    {
      category: 'விவாதம் & தீர்ப்பு',
      question: 'முரண்பாட்டு நடுவர் விவாத இயந்திரம் எவ்வாறு படைப்பு முட்டுக்கட்டைகளை தீர்க்கிறது?',
      answer: 'இரு துறைத் தலைவர்கள் இடையே கருத்து வேறுபாடு ஏற்படும் போது (எ.கா. ஒளிப்பதிவாளர் கோரும் 8K 120fps IMAX vs தயாரிப்பாளரின் பட்ஜெட் வரம்பு), தயாரிப்பாளர் அல்லது இயக்குனர் தலைமையில் பல சுற்று விவாதம் நடத்தப்பட்டு தொடர்ச்சியை பாதுகாக்கும் சமரசம் எட்டப்படுகிறது.'
    },
    {
      category: 'எதிரணி சோதனை',
      question: '5 எதிரணி (Red-Team) முகவர்கள் எவற்றை சோதிக்கின்றனர்?',
      answer: 'தயாரிப்பு திட்டங்களை படப்பிடிப்புக்கு முன் சோதிக்கின்றனர்: ANTG01 தேதி முரண்பாடுகள், ANTG02 பதிப்புரிமை வழக்குகள், ANTG03 கதை தொய்வு மற்றும் கிளிஷேக்கள், ANTG04 பைரசி கசிவு, ANTG05 மழை மற்றும் இயற்கை பேரழிவுகளை சோதிக்கிறது.'
    },
    {
      category: 'மல்டிமாடல் மீடியா',
      question: 'மல்டிமாடல் மீடியா ஸ்டுடியோ சினிமா சொத்துக்களை எவ்வாறு ஆய்வு செய்கிறது?',
      answer: 'Gemini 2.5 மற்றும் 3.8 Flash மூலம் திரைக்கதை தாள்கள் (OCR), ஸ்டோரிபோர்டு படங்கள், டால்பி அட்மோஸ் ஒலி அலைவரிசைகள் மற்றும் 24fps வீடியோ காட்சிகளை ஆய்வு செய்கிறது.'
    },
    {
      category: 'கண்காணிப்பு (Observability)',
      question: 'கிரஃபானா கிளவுட் MCP ஸ்ட்ரீமபிள் HTTP போக்குவரத்து எவ்வாறு செயல்படுகிறது?',
      answer: 'மாதிரி சூழல் நெறிமுறை (MCP) Streamable HTTP வழியாக நிகழ்நேர PromQL அளவீடுகள் (CDN 504 பிழைகள், CUDA VRAM), Tempo தடமறிதல் மற்றும் Loki பதிவுகளைப் பெற்று நேரடி கிரஃபானா டேஷ்போர்டுகளில் இயக்குனரின் தீர்வுகளை தானாக குறிக்கிறது.'
    }
  ],
  hi: [
    {
      category: 'आर्किटेक्चर और पात्र',
      question: 'थिरै कुझु एआई (திரை குழு AI) क्या है?',
      answer: 'थिरै कुझु एआई भारतीय और वैश्विक सिनेमा के लिए एक स्वायत्त, मल्टी-एजेंट फिल्म निर्माण ऑपरेटिंग सिस्टम और इंसिडेंट कमांड सेंटर है। यह 17 विभागों (369 पात्रों) में वास्तविक समय ग्राफना क्लाउड टेलीमेट्री के साथ संचालित होता है।'
    },
    {
      category: 'आर्किटेक्चर और पात्र',
      question: '17 बैंडों में 369 पात्रों को कैसे संरचित किया गया है?',
      answer: 'पात्रों को 17 स्टूडियो बैंडों (A: कार्यकारी, B: निर्देशन, C: पटकथा, D: कास्टिंग, E: सिनेमैटोग्राफी, F: कला, G: पोशाक, H: ध्वनि, I: स्टंट, J: VFX, K: संपादन, L: संगीत, M: डीआई, N: वितरण, O: कानूनी, P: विपणन, Q: वर्चुअल प्रोडक्शन) में व्यवस्थित किया गया है।'
    },
    {
      category: 'शासन और अधिकार',
      question: 'can_block: true और can_block: false में क्या अंतर है?',
      answer: 'can_block: true वाले पात्रों (निर्देशक B01, स्टंट मास्टर I01, कानूनी O01) के पास सुरक्षा या कॉपीराइट उल्लंघन पर शूटिंग रोकने का वीटो अधिकार होता है। can_block: false वाले सलाहकार के रूप में कार्य करते हैं।'
    },
    {
      category: 'डायनेमिक एसएमई',
      question: 'धारा 19 अनुबंध के तहत गतिशील एसएमई निर्माण कैसे काम करता है?',
      answer: 'जब दृश्य में विशेष डोमेन विशेषज्ञता (जैसे चोल कांस्य धातु विज्ञान, कक्षीय खगोल विज्ञान) की आवश्यकता होती है, तो धारा 19 के तहत गैर-अवरोधक सलाहकार तुरंत बनाए जाते हैं।'
    },
    {
      category: 'बहस और मध्यस्थता',
      question: 'द्वंद्वात्मक मध्यस्थता बहस इंजन रचनात्मक गतिरोधों को कैसे सुलझाता है?',
      answer: 'जब दो प्रमुखों के बीच मतभेद होते हैं (जैसे 8K IMAX बनाम बजट सीमा), तो कार्यकारी मध्यस्थ के नेतृत्व में बहु-चरणीय बहस के माध्यम से समाधान निकाला जाता है।'
    },
    {
      category: 'रेड-टीम परीक्षण',
      question: '5 रेड-टीम प्रतिपक्षी क्या अनुकरण करते हैं?',
      answer: 'वे उत्पादन योजनाओं का तनाव परीक्षण करते हैं: शेड्यूल ब्रेक, कॉपीराइट उल्लंघन, आलोचक प्रतिक्रिया, पायरेसी लीक, और मौसम संबंधी आपदाएं।'
    },
    {
      category: 'मल्टीमॉडल मीडिया',
      question: 'मल्टीमॉडल मीडिया स्टूडियो फिल्म संपत्तियों का निरीक्षण कैसे करता है?',
      answer: 'Gemini 2.5 और 3.8 Flash द्वारा संचालित, यह कॉल शीट (OCR), स्टोरीबोर्ड चित्र, डॉल्बी एटमॉस ऑडियो और 24fps वीडियो दैनिक फुटेज का विश्लेषण करता है।'
    },
    {
      category: 'अवलोकनशीलता (Observability)',
      question: 'ग्राफाना क्लाउड एमसीपी स्ट्रीमेबल HTTP ट्रांसपोर्ट कैसे काम करता है?',
      answer: 'मॉडल संदर्भ प्रोटोकॉल (MCP) के माध्यम से यह PromQL मेट्रिक्स, Tempo ट्रेस और Loki लॉग्स को ट्रैक करता है और लाइव डैशबोर्ड पर स्वचालित एनोटेशन दर्ज करता है।'
    }
  ],
  ja: [
    {
      category: 'アーキテクチャとペルソナ',
      question: 'Thirai Kuzhu AI（ティライ・クズAI）とは何ですか？',
      answer: 'Thirai Kuzhu AIは、映画製作のための自律型マルチエージェントOSおよびインシデントコマンドセンターです。17のスタジオ部門（369ペルソナ）をモデル化し、Grafana Cloud MCPリアルタイムテレメトリと統合されています。'
    },
    {
      category: 'アーキテクチャとペルソナ',
      question: '17のバンドにわたる369のペルソナはどのように構成されていますか？',
      answer: 'ペルソナは17の部門バンド（A: 製作総指揮、B: 監督、C: 脚本、D: キャスティング、E: 撮影、F: 美術、G: 衣装・メイク、H: 音響、I: アクション、J: VFX、K: 編集、L: 音楽、M: カラー、N: 配給、O: 法務、P: 宣伝、Q: バーチャルプロダクション）に分類されます。'
    },
    {
      category: 'ガバナンスと権限',
      question: 'can_block: true と can_block: false の明確な違いは何ですか？',
      answer: 'can_block: true（B01監督、I01スタント監督、O01法務など）を持つペルソナは、安全性や著作権違反時に撮影を即座に停止する拒否権を持ちます。can_block: false は助言のみを行います。'
    },
    {
      category: '動的SME専門家',
      question: '第19条契約に基づく動的専門家（SME）の合成はどのように機能しますか？',
      answer: '脚本のシーンで特殊な専門知識（古代青銅冶金学、軌道天体力学など）が必要な場合、can_block: false契約のもとで一時的な専門家がオンデマンドで生成されます。'
    },
    {
      category: '討論と仲裁',
      question: '弁証法仲裁ディベートエンジンは創造的な対立をどのように解決しますか？',
      answer: '部門長間で意見が対立した場合（例：8K 120fps IMAX撮影 vs 予算制限）、エグゼクティブ仲裁人のもとで多段階の討論を行い、拘束力のある解決策を導きます。'
    },
    {
      category: '敵対的テスト',
      question: '5つのレッドチーム敵対的エージェントは何をシミュレートしますか？',
      answer: '撮影前に計画をストレステストします：ANTG01スケジュール遅延、ANTG02著作権侵害、ANTG03批評家の酷評、ANTG04パイラシー流出、ANTG05異常気象。'
    },
    {
      category: 'マルチモーダルメディア',
      question: 'マルチモーダルメディアスタジオは映画アセットをどのように検査しますか？',
      answer: 'Gemini 2.5および3.8 Flashマルチモーダル推論により、脚本スキャン、絵コンテ、Dolby Atmos音声、24fpsデイリー映像を検査します。'
    },
    {
      category: '可観測性（Observability）',
      question: 'Grafana Cloud MCP Streamable HTTP トランスポートはどのように機能しますか？',
      answer: 'Model Context Protocol（MCP）を使用して、Prometheusメトリクス、Tempoトレース、Lokiログをストリーミングし、監督の緩和アノテーションをダッシュボードに自動挿入します。'
    }
  ],
  fr: [
    {
      category: 'Architecture & Personas',
      question: "Qu'est-ce que Thirai Kuzhu AI (திரை குழு AI) ?",
      answer: "Thirai Kuzhu AI est un système d'exploitation de production cinématographique multi-agents autonome et un centre de commandement d'incidents intégrant 369 personas répartis dans 17 départements avec télémétrie Grafana Cloud MCP."
    },
    {
      category: 'Architecture & Personas',
      question: 'Comment les 369 personas sont-ils structurés dans les 17 bandes ?',
      answer: 'Les personas sont organisés en 17 bandes (A: Production, B: Réalisation, C: Scénario, D: Casting, E: Image, F: Décors, G: Costumes, H: Son, I: Cascades, J: VFX, K: Montage, L: Musique, M: Étalonnage, N: Distribution, O: Juridique, P: Marketing, Q: Production Virtuelle).'
    },
    {
      category: 'Gouvernance & Autorité',
      question: 'Quelle est la différence stricte entre can_block: true et can_block: false ?',
      answer: 'Les rôles avec can_block: true (Réalisateur B01, Chef cascadeur I01, Juridique O01) possèdent un droit de veto pour interrompre le tournage en cas de violation. Ceux avec can_block: false agissent uniquement à titre consultatif.'
    },
    {
      category: 'Experts Dynamiques (SME)',
      question: "Comment fonctionne la synthèse d'experts selon la Section 19 ?",
      answer: "Lorsqu'une scène requiert une expertise rare (métallurgie Chola, astrodynamique), des experts éphémères sont matérialisés avec des outils en lecture seule et un contrat garanti can_block: false."
    },
    {
      category: 'Débat & Arbitrage',
      question: 'Comment le moteur de débat dialectique résout-il les désaccords créatifs ?',
      answer: "En cas d'impasse (ex. caméra IMAX 8K vs limites budgétaires), un débat structuré est arbitré par le Réalisateur ou le Producteur pour obtenir un compromis contraignant."
    },
    {
      category: 'Tests Adversariaux',
      question: 'Que simulent les 5 antagonistes Red-Team ?',
      answer: 'Ils éprouvent les plannings : conflits de dates acteurs (ANTG01), plagiat (ANTG02), faiblesses narratives (ANTG03), fuites de piratage (ANTG04) et météo extrême (ANTG05).'
    },
    {
      category: 'Médias Multimodaux',
      question: 'Comment le studio multimédia inspecte-t-il les rushes et les éléments ?',
      answer: 'Propulsé par Gemini 2.5 et 3.8 Flash, il analyse les feuilles de service, storyboards, pistes Dolby Atmos et rushes vidéo 24fps.'
    },
    {
      category: 'Observabilité',
      question: 'Comment fonctionne le transport Streamable HTTP Grafana Cloud MCP ?',
      answer: 'Il diffuse la télémétrie en temps réel (métriques Prometheus, traces Tempo, logs Loki) et injecte automatiquement des annotations de réalisation sur les tableaux de bord Grafana.'
    }
  ],
  te: [
    {
      category: 'ఆర్కిటెక్చర్ & పర్సనాలు',
      question: 'తిరై కుజు AI (Thirai Kuzhu AI) అంటే ఏమిటి?',
      answer: 'తిరై కుజు AI అనేది భారతీయ మరియు ప్రపంచ సినిమాల కోసం ఒక అటానమస్ మల్టీ-ఏజెంట్ ఫిల్మ్ ప్రొడక్షన్ ఆపరేటింగ్ సిస్టమ్ మరియు కమాండ్ సెంటర్. ఇది 17 విభాగాలలో 369 పాత్రలతో పనిచేస్తుంది.'
    },
    {
      category: 'ఆర్కిటెక్చర్ & పర్సనాలు',
      question: '17 బ్యాండ్లలో 369 పాత్రలు ఎలా నిర్వహించబడతాయి?',
      answer: 'పాత్రలు 17 విభాగ బ్యాండ్లుగా (ఎగ్జిక్యూటివ్, దర్శకత్వం, స్క్రిప్ట్, కాస్టింగ్, సినిమాటోగ్రఫీ, కళ, కాస్ట్యూమ్స్, ఆడియో, స్టంట్స్, VFX, ఎడిటింగ్, సంగీతం, కలరింగ్, డిస్ట్రిబ్యూషన్, లీగల్, మార్కెటింగ్, వర్చువల్ ప్రొడక్షన్) విభజించబడ్డాయి.'
    },
    {
      category: 'అధికారం & రూల్స్',
      question: 'can_block: true మరియు can_block: false మధ్య తేడా ఏమిటి?',
      answer: 'can_block: true కలిగిన దర్శకుడు, స్టంట్ డైరెక్టర్ వంటి వారు షూటింగ్‌ను నిలిపివేసే వీటో అధికారం కలిగి ఉంటారు. can_block: false కలిగిన వారు సలహాదారుగా మాత్రమే ఉంటారు.'
    },
    {
      category: 'డైనమిక్ నిపుణులు (SME)',
      question: 'సెక్షన్ 19 కింద డైనమిక్ SME నిర్మాణం ఎలా పనిచేస్తుంది?',
      answer: 'స్క్రిప్ట్‌కు లోహశాస్త్రం లేదా అంతరిక్ష భౌతికశాస్త్రం వంటి ప్రత్యేక పరిజ్ఞానం అవసరమైనప్పుడు, నాన్-బ్లాకింగ్ ఒప్పందంతో తాత్కాలిక నిపుణులు సృష్టించబడతారు.'
    },
    {
      category: 'చర్చ మరియు మధ్యవర్తిత్వం',
      question: 'ద్వంద్వ మధ్యవర్తిత్వ ఇంజిన్ సృజనాత్మక విభేదాలను ఎలా పరిష్కరిస్తుంది?',
      answer: 'విభాగ అధిపతుల మధ్య విభేదాలు వచ్చినప్పుడు, ఎగ్జిక్యూటివ్ మధ్యవర్తిత్వంలో బహుళ రౌండ్ల చర్చ ద్వారా పరిష్కారం సాధించబడుతుంది.'
    },
    {
      category: 'రెడ్ టీమ్ పరీక్షలు',
      question: '5 రెడ్-టీమ్ ఏజెంట్లు ఏమి పరీక్షిస్తారు?',
      answer: 'షూటింగ్‌కు ముందు షెడ్యూల్ సమస్యలు, కాపీరైట్ వివాదాలు, కథా లోపాలు, పైరసీ లీక్‌లు మరియు వాతావరణ విపత్తులను పరీక్షిస్తారు.'
    },
    {
      category: 'మల్టీమోడల్ మీడియా',
      question: 'మల్టీమోడల్ మీడియా స్టూడియో సినీ ఆస్తులను ఎలా విశ్లేషిస్తుంది?',
      answer: 'Gemini 2.5 మరియు 3.8 Flash ద్వారా కాల్ షీట్లు, స్టోరీబోర్డులు, డాల్బీ అట్మోస్ ఆడియో మరియు 24fps వీడియో ఫుటేజీలను పరిశీలిస్తుంది.'
    },
    {
      category: 'టెలిమెట్రీ',
      question: 'గ్రాఫానా క్లౌడ్ MCP స్ట్రీమబుల్ HTTP రవాణా ఎలా పనిచేస్తుంది?',
      answer: 'మోడల్ కాంటెక్స్ట్ ప్రోటోకాల్ (MCP) ద్వారా PromQL మెట్రిక్స్, Tempo ట్రేసెస్ మరియు Loki లాగ్‌లను లైవ్ డాష్‌బోర్డుల్లోకి ప్రసారం చేస్తుంది.'
    }
  ],
  de: [
    {
      category: 'Architektur & Rollen',
      question: 'Was ist Thirai Kuzhu AI (திரை குழு AI)?',
      answer: 'Thirai Kuzhu AI ist ein autonomes Multi-Agenten-Betriebssystem für Filmproduktionen und Einsatzleitzentrale mit 369 spezialisierten Rollen in 17 Abteilungen und Grafana-Cloud-Telemetrie.'
    },
    {
      category: 'Architektur & Rollen',
      question: 'Wie sind die 369 Personas auf die 17 Bänder aufgeteilt?',
      answer: 'Die Personas gliedern sich in 17 Bänder (A: Produktion, B: Regie, C: Drehbuch, D: Casting, E: Kamera, F: Szenenbild, G: Kostüm, H: Ton, I: Stunts, J: VFX, K: Schnitt, L: Musik, M: Grading, N: Verleih, O: Recht, P: Marketing, Q: Virtuelle Produktion).'
    },
    {
      category: 'Governance & Autorität',
      question: 'Was ist der Unterschied zwischen can_block: true und can_block: false?',
      answer: 'Rollen mit can_block: true (Regisseur B01, Stuntkoordinator I01, Justiziar O01) haben Veto-Rechte bei Sicherheits- oder Rechtsverletzungen. can_block: false agiert rein beratend.'
    },
    {
      category: 'Dynamische Experten (SME)',
      question: 'Wie funktioniert die Synthese dynamischer Fachexperten nach Paragraph 19?',
      answer: 'Bei speziellen Szenenanforderungen (z.B. historische Metallurgie, Astrodynamik) werden Berater mit Leserechten und verbindlicher Nicht-Blockierungs-Garantie instanziiert.'
    },
    {
      category: 'Debatte & Schlichtung',
      question: 'Wie löst die dialektische Schlichtung kreative Blockaden?',
      answer: 'Bei Zielkonflikten führt das System strukturierte Mehrrundendebatten unter Schlichtung von Regie oder Produktion durch.'
    },
    {
      category: 'Red-Team Stresstests',
      question: 'Was simulieren die 5 Red-Team Antagonisten?',
      answer: 'Terminkonflikte (ANTG01), Plagiatsklagen (ANTG02), dramaturgische Schwachstellen (ANTG03), Raubkopie-Lecks (ANTG04) und Unwetter/Höhere Gewalt (ANTG05).'
    },
    {
      category: 'Multimodale Medien',
      question: 'Wie analysiert das Multimodal Studio Filmmaterial?',
      answer: 'Mit Gemini 2.5 und 3.8 Flash prüft es Dispositionspläne (OCR), Storyboards, Dolby-Atmos-Audiodateien und 24fps-Tagesmuster.'
    },
    {
      category: 'Observability',
      question: 'Wie funktioniert der Grafana Cloud MCP Streamable HTTP Transport?',
      answer: 'Über das Model Context Protocol werden Prometheus-Metriken, Tempo-Traces und Loki-Logs gestreamt und automatisch im Grafana-Dashboard annotiert.'
    }
  ],
  es: [
    {
      category: 'Arquitectura y Personas',
      question: '¿Qué es Thirai Kuzhu AI (திரை குழு AI)?',
      answer: 'Thirai Kuzhu AI es un sistema operativo multi-agente autónomo de producción cinematográfica y centro de mando para cine global con 369 roles en 17 departamentos.'
    },
    {
      category: 'Arquitectura y Personas',
      question: '¿Cómo se estructuran los 369 roles en las 17 bandas?',
      answer: 'Se organizan en 17 bandas: A: Ejecutiva, B: Dirección, C: Guion, D: Casting, E: Cámara, F: Arte, G: Vestuario, H: Sonido, I: Acción, J: Efectos Visuales, K: Edición, L: Música, M: Color, N: Distribución, O: Legal, P: Publicidad, Q: Producción Virtual.'
    },
    {
      category: 'Gobernanza y Autoridad',
      question: '¿Cuál es la diferencia estricta entre can_block: true y can_block: false?',
      answer: 'Los roles con can_block: true (Director B01, Coordinador de Acción I01, Legal O01) tienen poder de veto para detener el rodaje por seguridad o derechos. can_block: false solo asesora.'
    },
    {
      category: 'Expertos Dinámicos (SME)',
      question: '¿Cómo funciona la creación de expertos dinámicos bajo la Sección 19?',
      answer: 'Cuando una escena requiere conocimiento específico (metalurgia antigua, astrodinámica), se generan especialistas efímeros con contrato no bloqueante.'
    },
    {
      category: 'Debate y Arbitraje',
      question: '¿Cómo resuelve el motor dialéctico los desacuerdos artísticos?',
      answer: 'Inicia debates estructurados arbitrados por el Productor o Director para alcanzar acuerdos vinculantes que protejan presupuesto y calidad.'
    },
    {
      category: 'Pruebas Adversariales',
      question: '¿Qué simulan los 5 antagonistas Red-Team?',
      answer: 'Colisiones de fechas (ANTG01), demandas de plagio (ANTG02), huecos de guion (ANTG03), filtraciones piratas (ANTG04) y desastres climáticos (ANTG05).'
    },
    {
      category: 'Medios Multimodales',
      question: '¿Cómo inspecciona los materiales cinematográficos?',
      answer: 'Mediante Gemini 2.5 y 3.8 Flash analiza órdenes de rodaje (OCR), storyboards, pistas de audio Dolby Atmos y tomas diarias a 24fps.'
    },
    {
      category: 'Observabilidad',
      question: '¿Cómo funciona el transporte Grafana Cloud MCP Streamable HTTP?',
      answer: 'Transmite métricas Prometheus, trazas Tempo y registros Loki, anotando soluciones directamente en los paneles de control de Grafana.'
    }
  ],
  ko: [
    {
      category: '아키텍처 및 페르소나',
      question: 'Thirai Kuzhu AI (திரை குழு AI)는 무엇인가요?',
      answer: 'Thirai Kuzhu AI는 글로벌 영화 제작을 위한 자율형 멀티에이전트 운영체제이자 인시던트 지휘 센터로, 17개 파트(369개 페르소나)와 실시간 Grafana Cloud MCP를 통합 지원합니다.'
    },
    {
      category: '아키텍처 및 페르소나',
      question: '17개 파트에 걸친 369개 페르소나는 어떻게 구성되어 있나요?',
      answer: '제작, 연출, 각본, 캐스팅, 촬영, 미술, 의상, 사운드, 무술, VFX, 편집, 음악, DI, 배급, 법무, 홍보, 버추얼 프로덕션 등 17개 파트로 나뉩니다.'
    },
    {
      category: '거버넌스 및 권한',
      question: 'can_block: true 와 can_block: false 의 명확한 차이는 무엇인가요?',
      answer: 'can_block: true 페르소나(감독 B01, 무술감독 I01, 법무 O01 등)는 안전이나 저작권 위반 시 촬영을 즉시 중단하는 거부권을 가집니다. can_block: false 는 자문 역할만 수행합니다.'
    },
    {
      category: '동적 전문 자문단 (SME)',
      question: '제19조 계약에 따른 동적 전문 자문단 합성은 어떻게 작동하나요?',
      answer: '특수 분야 검증이 필요한 경우, 읽기 전용 도구와 논블로킹(can_block: false) 계약을 통해 단기 전문 자문단을 온디맨드로 생성합니다.'
    },
    {
      category: '토론 및 중재',
      question: '변증법적 중재 토론 엔진은 창작 상의 갈등을 어떻게 해결하나요?',
      answer: '부서장 간 이견이 발생할 경우, 감독이나 제작자의 중재 하에 다단계 토론을 거쳐 예산과 일정을 지키는 구속력 있는 합의를 도출합니다.'
    },
    {
      category: '레드팀 스트레스 테스트',
      question: '5개의 레드팀 적대적 에이전트는 무엇을 시뮬레이션하나요?',
      answer: '배우 일정 충돌(ANTG01), 표절 소송(ANTG02), 서사적 결함(ANTG03), 불법 유출(ANTG04), 기상 악화(ANTG05)를 시뮬레이션합니다.'
    },
    {
      category: '멀티모달 미디어',
      question: '멀티모달 미디어 스튜디오는 영화 에셋을 어떻게 검사하나요?',
      answer: 'Gemini 2.5 및 3.8 Flash를 통해 콜시트(OCR), 스토리보드, Dolby Atmos 오디오, 24fps 일일 촬영 영상을 종합 분석합니다.'
    },
    {
      category: '관측성 (Observability)',
      question: 'Grafana Cloud MCP Streamable HTTP 전송은 어떻게 작동하나요?',
      answer: 'Model Context Protocol을 사용하여 Prometheus 메트릭, Tempo 트레이스, Loki 로그를 스트리밍하고 대시보드에 완화책을 자동 기록합니다.'
    }
  ],
  zh: [
    {
      category: '系统架构与角色',
      question: '什么是 Thirai Kuzhu AI (திரை குழு AI)？',
      answer: 'Thirai Kuzhu AI 是一套专为全球电影工业打造的自主多智能体电影制片操作系统与指挥调度中心，在17个制作梯队中组织369个智能体并对接 Grafana Cloud MCP。'
    },
    {
      category: '系统架构与角色',
      question: '369名智能体是如何分布在17个制作梯队的？',
      answer: '覆盖执行制片、导演、剧本、选角、摄影、美术、服化道、声音、特技、视效、剪辑、作曲、调色、发行、法务、营销及虚拟制作等17个专业部门。'
    },
    {
      category: '权限与治理体系',
      question: 'can_block: true 与 can_block: false 的严谨区别是什么？',
      answer: '拥有 can_block: true 的角色（如总导演 B01、特技指导 I01、首席法务 O01）拥有一票否决权，可在违规时立即叫停拍摄；can_block: false 的角色仅具备咨询与建议职能。'
    },
    {
      category: '动态领域专家 (SME)',
      question: '基于第19条协议的动态专家是如何生成的？',
      answer: '当剧本特定镜头需要冷门领域验证（如失蜡法冶金、天体力学）时，系统会在非阻塞性条款约束下即时生成只读咨询顾问。'
    },
    {
      category: '辩论与仲裁',
      question: '辩证仲裁引擎是如何化解艺术创作分歧的？',
      answer: '当两个制作部门发生意见冲突时，系统将在制片人或导演主持下组织多轮结构化辩论，达成兼顾预算与质量的终局裁决。'
    },
    {
      category: '红队混沌工程',
      question: '5个对抗性红队智能体模拟了哪些挑战？',
      answer: '包括档期冲突（ANTG01）、版权纠纷（ANTG02）、剧情节奏漏洞（ANTG03）、样片泄露（ANTG04）以及不可抗力极端天气（ANTG05）。'
    },
    {
      category: '多模态媒体工作室',
      question: '多模态媒体工作室如何审查影视资产？',
      answer: '基于 Gemini 2.5 与 3.8 Flash，对通告单（OCR）、分镜手稿、Dolby Atmos 全景声音频及 24fps 现场样片进行全方位质检。'
    },
    {
      category: '实时可观测性',
      question: 'Grafana Cloud MCP Streamable HTTP 协议是如何运作的？',
      answer: '借助模型上下文协议（MCP），将 Prometheus 指标、Tempo 分布式链路与 Loki 日志实时推送到 Grafana 监控大屏并打标处置建议。'
    }
  ],
  ar: [
    {
      category: 'الهندسة والشخصيات',
      question: 'ما هو Thirai Kuzhu AI (திரை குழு AI)؟',
      answer: 'هو أول نظام تشغيل سينمائي مستقل متعدد الوكلاء ومركز قيادة للحوادث مصمم للسينما العالمية ويغطي 369 شخصية عبر 17 قسماً متخصصاً مع مراقبة Grafana Cloud.'
    },
    {
      category: 'الهندسة والشخصيات',
      question: 'كيف يتم توزيع 369 شخصية عبر 17 فرقة إنتاج؟',
      answer: 'يتم تنظيمها في 17 فرقة: الإنتاج، الإخراج، السيناريو، التمثيل، التصوير، الديكور، الأزياء، الصوت، الحركات الخطرة، المؤثرات، المونتاج، الموسيقى، الألوان، التوزيع، القانون، التسويق، والإنتاج الافتراضي.'
    },
    {
      category: 'الحوكمة والسلطة',
      question: 'ما هو الفرق الدقيق بين can_block: true و can_block: false؟',
      answer: 'الشخصيات التي تمتلك can_block: true (مثل المخرج B01 ومستشار القانون O01) تتمتع بحق النقض لإيقاف التصوير فوراً عند حدوث خروقات. أما can_block: false فلها دور استشاري فقط.'
    },
    {
      category: 'الخبراء الديناميكيون (المادة 19)',
      question: 'كيف يعمل توليد الخبراء الديناميكيين بموجب المادة 19؟',
      answer: 'عندما يتطلب المشهد خبرة نادرة (علم الفلك أو المعادن القديمة)، يتم استدعاء مستشارين مؤقتين بأدوات للقراءة فقط وعقد غير مانع للتصوير.'
    },
    {
      category: 'المناظرة والتحكيم',
      question: 'كيف يحل محرك التحكيم الجدلي الخلافات الإبداعية؟',
      answer: 'عند حدوث خلاف بين رؤساء الأقسام، يُدار نقاش متعدد الجولات برئاسة المخرج أو المنتج للوصول إلى تسوية ملزمة تحافظ على الرؤية والميزانية.'
    },
    {
      category: 'اختبارات الفريق الأحمر',
      question: 'ماذا تحاكي شخصيات الفريق الأحمر الخمسة؟',
      answer: 'تضارب المواعيد (ANTG01)، دعاوى الانتحال (ANTG02)، ثغرات السيناريو (ANTG03)، تسريبات القرصنة (ANTG04)، والظروف الجوية القاسية (ANTG05).'
    },
    {
      category: 'الوسائط المتعددة',
      question: 'كيف يفحص استوديو الوسائط أصول الفيلم؟',
      answer: 'مدعوماً بـ Gemini 2.5 و 3.8 Flash، يفحص جداول التصوير ولوحات القصة ومسارات Dolby Atmos ومشاهد 24 إطاراً في الثانية.'
    },
    {
      category: 'المراقبة الفورية',
      question: 'كيف يعمل بروتوكول Grafana Cloud MCP Streamable HTTP؟',
      answer: 'ينقل القياسات المباشرة (Prometheus و Tempo و Loki) ويضيف تلقائياً ملاحظات وحلول المخرج على لوحات معلومات Grafana.'
    }
  ]
};

export function getLocalizedFaqs(lang) {
  if (LOCALIZED_FAQS[lang]) return LOCALIZED_FAQS[lang];
  if (lang === 'kn' || lang === 'ml') return LOCALIZED_FAQS.te || LOCALIZED_FAQS.ta || LOCALIZED_FAQS.en;
  if (lang === 'mr' || lang === 'bn' || lang === 'pa') return LOCALIZED_FAQS.hi || LOCALIZED_FAQS.en;
  if (lang === 'it' || lang === 'pt') return LOCALIZED_FAQS.es || LOCALIZED_FAQS.fr || LOCALIZED_FAQS.en;
  if (lang === 'zh-HK') return LOCALIZED_FAQS.zh || LOCALIZED_FAQS.en;
  return LOCALIZED_FAQS.en;
}
