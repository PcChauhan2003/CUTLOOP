import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # blank layout

    # Color Palette
    DARK_BG = RGBColor(10, 46, 35)      # Deep Emerald Green
    MINT = RGBColor(0, 200, 136)        # Vibrant Mint Green
    AMBER = RGBColor(255, 183, 3)       # Warm Gold/Amber
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252)  # Soft Slate 50
    CARD_BG = RGBColor(255, 255, 255)   # Crisp White Card
    CARD_BORDER = RGBColor(226, 232, 240)
    DARK_CARD = RGBColor(17, 65, 50)    # Elevated Dark Green
    TEXT_DARK = RGBColor(15, 23, 42)    # Slate 900
    TEXT_MUTED = RGBColor(100, 116, 139)# Slate 500
    TEXT_LIGHT = RGBColor(241, 245, 249)

    def set_slide_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="CUTLOOP CAPSTONE DEFENSE", dark_mode=False):
        # Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = MINT if dark_mode else RGBColor(16, 149, 103)

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = WHITE if dark_mode else TEXT_DARK

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: COVER SLIDE (DARK THEME)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, DARK_BG)

    # Badge Pill
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(3.6), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = DARK_CARD
    badge.line.color.rgb = MINT
    b_tf = badge.text_frame
    b_tf.margin_top = Inches(0.08)
    b_p = b_tf.paragraphs[0]
    b_p.text = "B.TECH CSE 5TH SEMESTER CAPSTONE"
    b_p.font.size = Pt(11)
    b_p.font.bold = True
    b_p.font.color.rgb = MINT
    b_p.alignment = PP_ALIGN.CENTER

    # Main Title
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(2.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "CUTLOOP"
    p1.font.size = Pt(56)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    p2.text = "AI-Powered Industrial Textile Waste Classification, Valuation & Circular Marketplace"
    p2.font.size = Pt(20)
    p2.font.color.rgb = MINT
    p2.space_before = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "\"One factory's leftover material is another creator's raw material.\""
    p3.font.size = Pt(14)
    p3.font.italic = True
    p3.font.color.rgb = AMBER
    p3.space_before = Pt(8)

    # 3 Subject Pillars on Slide 1
    pillars = [
        ("Java 21 Enterprise Core", "Atomic Order Transactions\nThreadPoolTaskExecutor\nCustom Exceptions\nRFC-4180 CSV Export"),
        ("Data Science & ML (47k)", "Cleaned 47,522 Garments\nBalanced Random Forest (88.2%)\nK-Means Clustering (k=5)\nMCX Hedonic Pricing Engine"),
        ("Deep Learning Vision", "TexSortML 11 Garment Classes\nMobileNetV2 (86.4% Acc)\nCustom CNN Baseline (72.2%)\nGrad-CAM Explainability")
    ]
    for i, (p_title, p_desc) in enumerate(pillars):
        c_left = Inches(0.8 + i * 3.9)
        c = add_card(s1, c_left, Inches(4.3), Inches(3.7), Inches(2.4), DARK_CARD, MINT)
        tb = s1.shapes.add_textbox(c_left + Inches(0.2), Inches(4.45), Inches(3.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = p_title
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE
        
        p_d = tf.add_paragraph()
        p_d.text = p_desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_LIGHT
        p_d.space_before = Pt(6)

    # Team Author Banner on Slide 1
    t_team = s1.shapes.add_textbox(Inches(0.8), Inches(6.85), Inches(11.5), Inches(0.45))
    tf_team = t_team.text_frame
    p_team = tf_team.paragraphs[0]
    p_team.text = "JG University · Department of Computer Science & Engineering | Team: Prem Chauhan (Lead) · Kanjariya Jay · Parthik Desai · Vivek Prajapati · Parth Agravat"
    p_team.font.size = Pt(11)
    p_team.font.bold = True
    p_team.font.color.rgb = MINT
    p_team.alignment = PP_ALIGN.CENTER

    s1.notes_slide.notes_text_frame.text = (
        "Good morning evaluators. My name is Prem Chauhan, Lead Presenter, and on behalf of our team—Kanjariya Jay, Parthik Desai, Vivek Prajapati, and Parth Agravat—we present CUTLOOP—an integrated AI-powered circular marketplace connecting "
        "industrial textile mills liquidating surplus remnants with sustainable creators seeking affordable, verified raw materials. "
        "Our submission brings together Java 21 enterprise backend services, data science on 47,000+ records, and dual deep learning vision models."
    )

    # =========================================================================
    # SLIDE 2: THE INDUSTRIAL CRISIS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, LIGHT_BG)
    add_header(s2, "The Pre-Consumer Textile Waste Crisis in India")

    # 3 Stat Cards
    stat_data = [
        ("1.4 Million Tonnes", "Annual Indian Pre-Consumer Waste", "Discarded across Ahmedabad, Surat, Tirupur & Ludhiana industrial manufacturing hubs."),
        ("12% to 22%", "Virgin Fabric Lost on Cutting Tables", "Offcuts, sampling remnants & deadstock rolls lost during pattern cutting."),
        ("500 kg MOQ", "Minimum Order Barrier for Creators", "Small artisan studios forced to pay 100% full virgin retail prices for small yardages.")
    ]
    for i, (num, sub, desc) in enumerate(stat_data):
        c_left = Inches(0.8 + i * 3.9)
        add_card(s2, c_left, Inches(1.8), Inches(3.7), Inches(1.8), CARD_BG)
        tb = s2.shapes.add_textbox(c_left + Inches(0.2), Inches(1.9), Inches(3.3), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p_num = tf.paragraphs[0]
        p_num.text = num
        p_num.font.size = Pt(24)
        p_num.font.bold = True
        p_num.font.color.rgb = RGBColor(16, 149, 103)
        
        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(12)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_DARK
        p_sub.space_before = Pt(2)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = TEXT_MUTED
        p_desc.space_before = Pt(4)

    # 2 Comparison Columns (Factory Bottleneck vs Creator Bottleneck)
    add_card(s2, Inches(0.8), Inches(3.9), Inches(5.7), Inches(3.0), CARD_BG)
    tb_fac = s2.shapes.add_textbox(Inches(1.0), Inches(4.05), Inches(5.3), Inches(2.7))
    tf_f = tb_fac.text_frame
    tf_f.word_wrap = True
    pf_title = tf_f.paragraphs[0]
    pf_title.text = "Factory & Mill Pain Points"
    pf_title.font.size = Pt(16)
    pf_title.font.bold = True
    pf_title.font.color.rgb = RGBColor(220, 38, 38)
    
    fac_bullets = [
        "Sinking warehouse costs: Deadstock rolls accumulate dust, pest damage, and lock capital.",
        "Zero digital channel: Selling small 20-100 kg scrap lots is too slow and labor-intensive.",
        "Informal exploitation: 'Chindi' scrap traders pay arbitrary pennies per kilogram.",
        "Destructive disposal: Mills resort to paying haulers for landfilling or open incineration."
    ]
    for b in fac_bullets:
        p = tf_f.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(5)

    add_card(s2, Inches(6.8), Inches(3.9), Inches(5.7), Inches(3.0), CARD_BG)
    tb_cre = s2.shapes.add_textbox(Inches(7.0), Inches(4.05), Inches(5.3), Inches(2.7))
    tf_c = tb_cre.text_frame
    tf_c.word_wrap = True
    pc_title = tf_c.paragraphs[0]
    pc_title.text = "Artisan & Sustainable Creator Pain Points"
    pc_title.font.size = Pt(16)
    pc_title.font.bold = True
    pc_title.font.color.rgb = RGBColor(37, 99, 235)
    
    cre_bullets = [
        "Extreme cost barrier: Forced to buy virgin retail fabrics at 100% full markup.",
        "Minimum order rejection: Cannot meet mill 500+ kg production minimums.",
        "Zero transparency: No verification of fabric composition, tensile strength, or hidden flaws.",
        "Severe sourcing friction: Traveling across remote industrial estates with no quality guarantee."
    ]
    for b in cre_bullets:
        p = tf_c.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(5)

    s2.notes_slide.notes_text_frame.text = (
        "Between 12% and 22% of virgin textile material never becomes apparel. Discarded remnants sit idle in warehouses, "
        "costing factories monthly storage while locking working capital. Small creators cannot buy small batches without paying full retail. "
        "CUTLOOP eliminates this inefficiency by bridging supply and demand with AI verification."
    )

    # =========================================================================
    # SLIDE 3: THE CUTLOOP SOLUTION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, LIGHT_BG)
    add_header(s3, "The CUTLOOP Solution: Automated Waste-to-Value in 60 Seconds")

    solution_pillars = [
        ("1. Instant Camera Scan", "Factory supervisor snaps a photo of scrap rolls using any smartphone. No lab setup or manual typing required."),
        ("2. Computer Vision AI", "Fine-tuned MobileNetV2 classifies apparel garment category (11 classes) with 86.4% test accuracy in 35ms."),
        ("3. NLP Fiber Extraction", "Balanced Random Forest extracts fiber composition (Cotton, Poly, Nylon, Wool) with 88.2% test accuracy."),
        ("4. Circular Recycling Router", "K-Means model (k=5, Silhouette: 0.6686) assigns the fabric to an industrial recycling stream (e.g. Garnetting)."),
        ("5. MCX Hedonic Pricing", "Algorithmic valuation linked to Multi Commodity Exchange Cotton spot index recommends an immediate fair clearing price."),
        ("6. Atomic Escrow B2B Market", "Spring Boot handles atomic transactions, prevents overselling via custom exceptions, and tracks 5-stage logistics.")
    ]

    for i, (title, desc) in enumerate(solution_pillars):
        row = i // 3
        col = i % 3
        c_left = Inches(0.8 + col * 3.9)
        c_top = Inches(1.8 + row * 2.6)
        add_card(s3, c_left, c_top, Inches(3.7), Inches(2.3), CARD_BG)
        tb = s3.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.15), Inches(3.3), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = RGBColor(16, 149, 103)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_DARK
        p_d.space_before = Pt(6)

    s3.notes_slide.notes_text_frame.text = (
        "Our solution replaces tedious manual cataloging. A factory worker takes a smartphone photo. In 35 milliseconds, "
        "our deep learning vision model classifies the category, our NLP model infers composition, K-Means assigns the circular pathway, "
        "and our valuation engine computes a fair price. With one click, the listing is live."
    )

    # =========================================================================
    # SLIDE 4: MARKET OPPORTUNITY & PERSONAS
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, LIGHT_BG)
    add_header(s4, "Market Opportunity (TAM / SAM / SOM) & Target Users")

    # Left: Market Sizing
    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), CARD_BG)
    tb_m = s4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    pm_title = tf_m.paragraphs[0]
    pm_title.text = "Market Size Breakdown"
    pm_title.font.size = Pt(18)
    pm_title.font.bold = True
    pm_title.font.color.rgb = RGBColor(16, 149, 103)

    market_tiers = [
        ("TAM: $165 Billion", "Total Indian Industrial Textile & Apparel Sector", "India is the 2nd largest global textile exporter with an immense manufacturing base."),
        ("SAM: $4.2 Billion", "Pre-Consumer Textile Waste & Remnants", "The aggregate value of cutting scraps, roll offcuts, and mill deadstock generated annually."),
        ("SOM: $45 Million", "5-Year Target in Gujarat & Tamil Nadu Hubs", "Focusing on Narol, Vatva, Surat GIDC, and Tirupur knitwear manufacturing clusters.")
    ]
    for tier, sub, desc in market_tiers:
        p_t = tf_m.add_paragraph()
        p_t.text = tier
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_DARK
        p_t.space_before = Pt(10)
        
        p_s = tf_m.add_paragraph()
        p_s.text = sub
        p_s.font.size = Pt(11)
        p_s.font.bold = True
        p_s.font.color.rgb = RGBColor(16, 149, 103)
        
        p_d = tf_m.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    # Right: User Personas
    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), CARD_BG)
    tb_p = s4.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    pp_title = tf_p.paragraphs[0]
    pp_title.text = "Core Stakeholder Personas"
    pp_title.font.size = Pt(18)
    pp_title.font.bold = True
    pp_title.font.color.rgb = RGBColor(37, 99, 235)

    personas = [
        ("Sellers: Weaving Mills & Garment Exporters", [
            "500+ composite mills and cut-and-sew garment export units in Gujarat & Tamil Nadu.",
            "Motivation: Monetize locked warehouse space, turn scrap into cash, meet zero-waste audits.",
            "Key Feature: 1-click photo upload, automated pricing, scheduled hub pickup."
        ]),
        ("Buyers: Sustainable Creators & Recyclers", [
            "Eco-fashion startups, upcycling studios, handicraft artisans, student designers.",
            "Motivation: Sourcing verified high-grade fabrics at 40%–60% below virgin retail rates.",
            "Key Feature: Multi-attribute compatibility matching, escrow protection, low-volume batches."
        ])
    ]
    for p_name, p_bullets in personas:
        p_t = tf_p.add_paragraph()
        p_t.text = p_name
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_DARK
        p_t.space_before = Pt(12)
        for b in p_bullets:
            p_b = tf_p.add_paragraph()
            p_b.text = "• " + b
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = TEXT_MUTED
            p_b.space_before = Pt(3)

    s4.notes_slide.notes_text_frame.text = (
        "Textile waste is an enormous $4.2 Billion serviceable market. Our 5-year target focuses on Gujarat and Tamil Nadu. "
        "We serve two balanced sides: mills liquidating warehouse scrap to free working capital, and creators acquiring circular materials at deep discounts."
    )

    # =========================================================================
    # SLIDE 5: SYSTEM ARCHITECTURE (JAVA + FASTAPI)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, LIGHT_BG)
    add_header(s5, "Enterprise Polyglot Architecture (Java 21 & Python FastAPI)")

    arch_blocks = [
        ("Presentation Layer", "Port 3000 Client", [
            "Responsive HTML5, ES6 JavaScript, and inlined critical CSS3.",
            "Zero-dropout mobile architecture eliminates CSS network loss over tunnels.",
            "Live Cloudflare Tunnel & localhost.run fallback deployment."
        ]),
        ("Backend Core", "Java 21 / Spring Boot 3", [
            "Domain Hierarchy: Abstract TextileMaterial extended by 3 lot types.",
            "Atomic Concurrency: Isolation.SERIALIZABLE prevents double-purchasing.",
            "Custom Domain Exceptions: InsufficientStockException rollback.",
            "Multithreading: ThreadPoolTaskExecutor (4 core, 8 max threads).",
            "Streaming CSV File I/O: Memory-efficient RFC-4180 inventory exports."
        ]),
        ("AI Microservice", "Python FastAPI (Port 8000)", [
            "Model A (NLP): Balanced Random Forest Dominant Fiber Classifier.",
            "Model B (Vision): MobileNetV2 11-category apparel classifier.",
            "Model C (Cluster): K-Means (k=5) circular recycling stream router.",
            "Model D (Valuation): Hedonic MCX commodity price clearing engine.",
            "Grad-CAM Heatmaps: Visual feature explainability."
        ])
    ]

    for i, (b_tag, b_title, b_items) in enumerate(arch_blocks):
        c_left = Inches(0.8 + i * 3.9)
        add_card(s5, c_left, Inches(1.8), Inches(3.7), Inches(5.1), CARD_BG)
        tb = s5.shapes.add_textbox(c_left + Inches(0.2), Inches(2.0), Inches(3.3), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p_tag = tf.paragraphs[0]
        p_tag.text = b_tag.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = RGBColor(16, 149, 103)
        
        p_t = tf.add_paragraph()
        p_t.text = b_title
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_DARK
        p_t.space_before = Pt(4)

        for item in b_items:
            p = tf.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MUTED
            p.space_before = Pt(6)

    s5.notes_slide.notes_text_frame.text = (
        "We implemented a decoupled polyglot microservice architecture. Java Spring Boot guarantees enterprise transaction integrity, "
        "atomic inventory reservations, and multithreading, while Python FastAPI hosts our PyTorch and Scikit-Learn models on port 8000."
    )

    # =========================================================================
    # SLIDE 6: PRODUCT WORKFLOW & LIFE-CYCLE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, LIGHT_BG)
    add_header(s6, "End-to-End Product Workflow: The 6-Stage Marketplace Lifecycle")

    steps = [
        ("01", "Snap & Upload", "Factory worker photographs textile remnant roll using smartphone; UI forwards image to FastAPI."),
        ("02", "AI Processing", "MobileNetV2 detects garment category; Random Forest extracts fiber; K-Means assigns recycling archetype."),
        ("03", "Hedonic Valuation", "Hedonic formula computes fair clearing price (e.g. ₹48.50/kg) based on MCX cotton index and purity."),
        ("04", "Marketplace Publish", "Seller approves suggested price with 1 click; listing goes live with verified circularity badges."),
        ("05", "Multi-Attribute Match", "Buyer searches via weighted formula: Score = 0.35M + 0.25P + 0.20Q + 0.10C + 0.10L."),
        ("06", "Atomic Checkout", "Spring Boot executes atomic inventory decrement; funds held in simulated escrow across 5 hub tracking stages.")
    ]

    for i, (num, title, desc) in enumerate(steps):
        row = i // 3
        col = i % 3
        c_left = Inches(0.8 + col * 3.9)
        c_top = Inches(1.8 + row * 2.6)
        add_card(s6, c_left, c_top, Inches(3.7), Inches(2.3), CARD_BG)
        tb = s6.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.15), Inches(3.3), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_num = tf.paragraphs[0]
        p_num.text = num
        p_num.font.size = Pt(22)
        p_num.font.bold = True
        p_num.font.color.rgb = RGBColor(16, 149, 103)

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_DARK
        p_t.space_before = Pt(2)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(4)

    s6.notes_slide.notes_text_frame.text = (
        "Here is the user journey in action: The seller uploads a photo. The AI pipeline extracts specs, classifies the circular archetype, "
        "and suggests a price. With one click, it is published. A buyer finds it using our multi-attribute matcher, checks out through escrow, "
        "and tracks fulfillment through 5 regional hub milestones."
    )

    # =========================================================================
    # SLIDE 7: DATA SCIENCE & EDA FINDINGS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, LIGHT_BG)
    add_header(s7, "Data Science Life-Cycle: 47,522 Garments Analyzed")

    # Left: Cleaning Pipeline Card
    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), CARD_BG)
    tb_d = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True
    pd_title = tf_d.paragraphs[0]
    pd_title.text = "Dataset Ingestion & Feature Engineering"
    pd_title.font.size = Pt(17)
    pd_title.font.bold = True
    pd_title.font.color.rgb = RGBColor(16, 149, 103)

    pipeline_bullets = [
        "Raw Volume: 47,522 fast-fashion garment records parsed from nested multi-component JSON structures.",
        "10D Fiber Space: Normalized continuous vector summing to 100%: [Cotton, Poly, Elastane, Nylon, Viscose, Wool, Acrylic, Linen, Silk, Other].",
        "Zero-Imputation: Missing component percentages imputed with 0.0%; deduplicated parent items to eliminate duplicate skewness.",
        "Target Leakage Safeguard: Numerical circularity metrics and target fiber labels strictly excluded from feature inputs.",
        "Stratified Splits: 80% Train (N=38,017) and 20% Held-Out Test (N=9,505) seeded with random_state=42."
    ]
    for b in pipeline_bullets:
        p = tf_d.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(8)

    # Right: Statistical & Blend Insights
    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), CARD_BG)
    tb_s = s7.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True
    ps_title = tf_s.paragraphs[0]
    ps_title.text = "Dominant Fibers & Blending Bottlenecks"
    ps_title.font.size = Pt(17)
    ps_title.font.bold = True
    ps_title.font.color.rgb = RGBColor(37, 99, 235)

    stats_insights = [
        ("Cotton Dominance (50.5%):", "23,985 records. Dominates t-shirts, casual tops, denim jeans, and underwear. Mean content when present: 92.4%."),
        ("Polyester Synthetics (27.7%):", "13,176 records. Predominates in dresses, outerwear shells, and lining fabrics. Mean content: 86.1%."),
        ("58.2% Mono-Materials (27,658 items):", "Garments with >=95% single fiber purity. Prime candidates for direct mechanical shredding and garnetting."),
        ("41.8% Intimate Blends (19,864 items):", "Binary and ternary blends. Over 72% contain elastane/Spandex (1%-5%), creating major recycling separation bottlenecks.")
    ]
    for title, desc in stats_insights:
        p_t = tf_s.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_DARK
        p_t.space_before = Pt(8)
        
        p_d = tf_s.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(2)

    s7.notes_slide.notes_text_frame.text = (
        "Our data science analysis on 47,522 garment records revealed critical industrial insights: 58.2% are mono-materials, "
        "but 41.8% are intimate blends. Over 72% of blends contain elastane, presenting massive barriers for recyclers that CUTLOOP's archetype clustering solves."
    )

    # =========================================================================
    # SLIDE 8: MACHINE LEARNING BASELINES & CLUSTERING
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, LIGHT_BG)
    add_header(s8, "Model A (NLP Fiber) & Model C (K-Means Archetypes)")

    # Left: Model A Comparison Table
    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), CARD_BG)
    tb_a = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_a = tb_a.text_frame
    tf_a.word_wrap = True
    pa_title = tf_a.paragraphs[0]
    pa_title.text = "Model A: Supervised Fiber Classifier"
    pa_title.font.size = Pt(16)
    pa_title.font.bold = True
    pa_title.font.color.rgb = RGBColor(16, 149, 103)

    pa_sub = tf_a.add_paragraph()
    pa_sub.text = "Evaluated on Held-Out Test Set (N=9,505, 413 Features)"
    pa_sub.font.size = Pt(11)
    pa_sub.font.color.rgb = TEXT_MUTED

    model_a_stats = [
        ("Overall Test Accuracy:", "Decision Tree: 78.09%  ->  Random Forest: 88.15% (+10.06%)"),
        ("Macro-Averaged F1:", "Decision Tree: 0.7036  ->  Random Forest: 0.8257 (+0.1221)"),
        ("Weighted F1-Score:", "Decision Tree: 0.7854  ->  Random Forest: 0.8837 (+0.0983)"),
        ("Wool Class F1:", "Decision Tree: 0.68  ->  Random Forest: 0.83 (+0.1500)"),
        ("Linen Class F1:", "Decision Tree: 0.79  ->  Random Forest: 0.91 (+0.1200)"),
        ("Polyamide Class F1:", "Decision Tree: 0.69  ->  Random Forest: 0.82 (+0.1300)")
    ]
    for metric, val in model_a_stats:
        p_m = tf_a.add_paragraph()
        p_m.text = metric
        p_m.font.size = Pt(11)
        p_m.font.bold = True
        p_m.font.color.rgb = TEXT_DARK
        p_m.space_before = Pt(6)
        
        p_v = tf_a.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(10)
        p_v.font.color.rgb = RGBColor(16, 149, 103)

    # Right: Model C K-Means Archetypes
    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), CARD_BG)
    tb_c = s8.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    pc_title = tf_c.paragraphs[0]
    pc_title.text = "Model C: 5 Circular Material Archetypes"
    pc_title.font.size = Pt(16)
    pc_title.font.bold = True
    pc_title.font.color.rgb = RGBColor(37, 99, 235)

    pc_sub = tf_c.add_paragraph()
    pc_sub.text = "Peak Global Silhouette = 0.6686 (Optimal k=5 Sweep)"
    pc_sub.font.size = Pt(11)
    pc_sub.font.color.rgb = TEXT_MUTED

    archetypes = [
        ("Archetype 0 (Cotton Mono - 50.0%):", "89.3% Cotton, 6.1% Poly -> Mechanical Garnetting"),
        ("Archetype 1 (Synthetic Poly - 27.3%):", "82.9% Poly, 3.8% Elastane -> Chemical Glycolysis"),
        ("Archetype 2 (Technical Stretch - 6.7%):", "84.1% Nylon, 12.6% Elastane -> Polymer Re-extrusion"),
        ("Archetype 3 (Cellulosic Blends - 7.7%):", "71.9% Viscose, 9.7% Nylon -> Solvent Dissolution"),
        ("Archetype 4 (Animal Wool - 8.2%):", "23.5% Wool, 12.9% Acrylic -> Shoddy Yarn Spinning")
    ]
    for arch, pathway in archetypes:
        p_a = tf_c.add_paragraph()
        p_a.text = arch
        p_a.font.size = Pt(11)
        p_a.font.bold = True
        p_a.font.color.rgb = TEXT_DARK
        p_a.space_before = Pt(7)
        
        p_p = tf_c.add_paragraph()
        p_p.text = pathway
        p_p.font.size = Pt(10)
        p_p.font.color.rgb = RGBColor(37, 99, 235)

    s8.notes_slide.notes_text_frame.text = (
        "In Model A, our Balanced Random Forest outperformed the Decision Tree baseline across every metric, "
        "gaining +10.06% in accuracy. In Model C, our silhouette sweep across k=2 to 8 proved k=5 reached the global peak at 0.6686, "
        "cleanly isolating the 5 industrial circular recycling streams."
    )

    # =========================================================================
    # SLIDE 9: DEEP LEARNING VISION BENCHMARK
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, LIGHT_BG)
    add_header(s9, "Deep Learning: MobileNetV2 (86.4%) vs Custom CNN (72.2%)")

    # Left: Benchmark Metrics Table
    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), CARD_BG)
    tb_b = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    pb_title = tf_b.paragraphs[0]
    pb_title.text = "Held-Out Test Set Performance (N=338)"
    pb_title.font.size = Pt(16)
    pb_title.font.bold = True
    pb_title.font.color.rgb = RGBColor(16, 149, 103)

    dl_metrics = [
        ("Held-Out Test Accuracy:", "Custom CNN: 72.19%  ->  MobileNetV2: 86.39% (+14.20% Gain)"),
        ("Macro-Averaged F1:", "Custom CNN: 0.6503  ->  MobileNetV2: 0.8015 (+0.1512 Gain)"),
        ("Weighted-Averaged F1:", "Custom CNN: 0.6988  ->  MobileNetV2: 0.8604 (+0.1616 Gain)"),
        ("Macro-Averaged Recall:", "Custom CNN: 0.6492  ->  MobileNetV2: 0.8087 (+0.1595 Gain)"),
        ("Dress Recall:", "Custom CNN: 32.00%  ->  MobileNetV2: 92.00% (+60.00% Gain)"),
        ("CPU Inference Latency:", "Custom CNN: ~18 ms  ->  MobileNetV2: ~35 ms per image")
    ]
    for metric, val in dl_metrics:
        p_m = tf_b.add_paragraph()
        p_m.text = metric
        p_m.font.size = Pt(11)
        p_m.font.bold = True
        p_m.font.color.rgb = TEXT_DARK
        p_m.space_before = Pt(6)
        
        p_v = tf_b.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(10)
        p_v.font.color.rgb = RGBColor(16, 149, 103)

    # Right: Error Diagnosis & Grad-CAM
    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), CARD_BG)
    tb_g = s9.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_g = tb_g.text_frame
    tf_g.word_wrap = True
    pg_title = tf_g.paragraphs[0]
    pg_title.text = "Error Diagnosis & Grad-CAM Explainability"
    pg_title.font.size = Pt(16)
    pg_title.font.bold = True
    pg_title.font.color.rgb = RGBColor(37, 99, 235)

    dl_insights = [
        ("Why Custom CNN Collapsed on Dresses (32% Recall):", [
            "A dress requires long-range vertical receptive field (neckline to hem).",
            "Custom 4-block CNN has only a 31x31 pixel receptive field before pooling.",
            "Encountering dress bodices, it confused them with collared polo shirts.",
            "MobileNetV2's 53 layers synthesize global full-length spatial context."
        ]),
        ("Grad-CAM Convolutional Heatmaps:", [
            "Calculated at the final Conv_1 inverted bottleneck layer.",
            "Activations concentrate on collars, sleeve joins, waistbands, and hemlines.",
            "Proves the model inspects garment structure rather than floor artifacts."
        ])
    ]
    for title, bullets in dl_insights:
        p_t = tf_g.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_DARK
        p_t.space_before = Pt(8)
        for b in bullets:
            p_b = tf_g.add_paragraph()
            p_b.text = "• " + b
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = TEXT_MUTED
            p_b.space_before = Pt(2)

    s9.notes_slide.notes_text_frame.text = (
        "We scientifically proved the value of transfer learning. MobileNetV2 achieved 86.39% accuracy—outperforming our Custom CNN by +14.2%. "
        "We diagnosed why: the Custom CNN's small receptive field caused dress recall to collapse to 32%, mistaking bodices for shirts. "
        "MobileNetV2's deep architecture captured the full geometry."
    )

    # =========================================================================
    # SLIDE 10: BUSINESS MODEL & UNIT ECONOMICS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, LIGHT_BG)
    add_header(s10, "Business Model, Revenue Streams & Unit Economics")

    # Left: Revenue Streams
    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), CARD_BG)
    tb_r = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    pr_title = tf_r.paragraphs[0]
    pr_title.text = "Core Monetization Channels"
    pr_title.font.size = Pt(17)
    pr_title.font.bold = True
    pr_title.font.color.rgb = RGBColor(16, 149, 103)

    streams = [
        ("5% Seller Commission", "Deducted automatically upon confirmed delivery on order Gross Merchandise Value (GMV)."),
        ("Logistics Fulfillment Margin", "Flat ₹150 base delivery fee + weight tier handling margin across 4 regional textile hubs."),
        ("Enterprise SaaS Subscription", "₹1,999/month for composite textile mills requiring automated CSV inventory sync, buyer matching, and demand forecasting."),
        ("Quality Certification Fee", "₹499 per physical swatch lab verification for high-value export remnants.")
    ]
    for name, desc in streams:
        p_n = tf_r.add_paragraph()
        p_n.text = name
        p_n.font.size = Pt(12)
        p_n.font.bold = True
        p_n.font.color.rgb = TEXT_DARK
        p_n.space_before = Pt(8)
        
        p_d = tf_r.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(2)

    # Right: Unit Economics (100 kg Lot)
    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), CARD_BG)
    tb_u = s10.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_u = tb_u.text_frame
    tf_u.word_wrap = True
    pu_title = tf_u.paragraphs[0]
    pu_title.text = "Unit Economics (Typical 100 kg Lot)"
    pu_title.font.size = Pt(17)
    pu_title.font.bold = True
    pu_title.font.color.rgb = RGBColor(37, 99, 235)

    econ_items = [
        ("Gross Order GMV (100 kg @ ₹50/kg):", "₹5,000"),
        ("5% Platform Commission:", "+ ₹250"),
        ("Net Logistics Handling Margin:", "+ ₹75"),
        ("Net Platform Revenue per Order:", "₹325 (6.5% Net Take Rate)"),
        ("Factory Onboarding CAC (GIDC estate):", "₹850 (One-time field visit)"),
        ("Recurring Order Volume:", "12 orders / month per factory"),
        ("Monthly Net Platform Profit:", "₹3,900 per mill"),
        ("Payback Period & 1-Year LTV:CAC:", "< 30 Days  |  LTV:CAC = 55:1")
    ]
    for label, val in econ_items:
        p_l = tf_u.add_paragraph()
        p_l.text = label
        p_l.font.size = Pt(11)
        p_l.font.bold = True
        p_l.font.color.rgb = TEXT_DARK
        p_l.space_before = Pt(5)
        
        p_v = tf_u.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(11)
        p_v.font.bold = True
        p_v.font.color.rgb = RGBColor(16, 149, 103) if "+" in val or "325" in val or "55:1" in val else TEXT_MUTED

    s10.notes_slide.notes_text_frame.text = (
        "Our business model is lean and scalable. We charge a 5% commission plus fulfillment margin, netting ₹325 on a typical 100 kg order. "
        "Because textile mills generate continuous cutting waste every single week, the customer payback period is under 30 days, "
        "yielding an LTV-to-CAC ratio exceeding 50 to 1."
    )

    # =========================================================================
    # SLIDE 11: SEED BUDGET & DPIIT ROADMAP
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11, LIGHT_BG)
    add_header(s11, "₹50,000 Academic Seed Budget & Startup Roadmap")

    # Left: Budget Allocation Table
    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), CARD_BG)
    tb_bd = s11.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_bd = tb_bd.text_frame
    tf_bd.word_wrap = True
    pbd_title = tf_bd.paragraphs[0]
    pbd_title.text = "₹50,000 Seed Budget Allocation"
    pbd_title.font.size = Pt(17)
    pbd_title.font.bold = True
    pbd_title.font.color.rgb = RGBColor(16, 149, 103)

    budget_breakdown = [
        ("Cloud Staging & Hosting:", "₹20,000 (Domain, SSL, database compute, Netlify CDN)"),
        ("Factory Field Trials & Annotation:", "₹10,000 (Collecting & annotating 1,200 real factory samples)"),
        ("Sample Swatch Logistics & Beta:", "₹10,000 (Fulfilling test swatch deliveries for 20 beta creators)"),
        ("DPIIT Registration & Compliance:", "₹5,000 (Pvt. Ltd. incorporation & Class 35 trademark filing)"),
        ("Emergency Contingency Buffer:", "₹5,000 (Operational reserve fund)"),
        ("Total Prototype Budget:", "₹50,000 (Fully accounted academic bootstrapping)")
    ]
    for cat, desc in budget_breakdown:
        p_c = tf_bd.add_paragraph()
        p_c.text = cat
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = TEXT_DARK
        p_c.space_before = Pt(6)
        
        p_d = tf_bd.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    # Right: 3-Phase Roadmap
    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), CARD_BG)
    tb_rm = s11.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_rm = tb_rm.text_frame
    tf_rm.word_wrap = True
    prm_title = tf_rm.paragraphs[0]
    prm_title.text = "Strategic Milestone Roadmap"
    prm_title.font.size = Pt(17)
    prm_title.font.bold = True
    prm_title.font.color.rgb = RGBColor(37, 99, 235)

    phases = [
        ("Phase 1: Cluster Onboarding (Months 1-3)", [
            "Deploy production cloud instance; onboard 25 mills in Ahmedabad & Surat.",
            "Catalog 5,000 kg of cutting remnants; achieve 50 completed transactions."
        ]),
        ("Phase 2: DPIIT & Grant Scaling (Months 4-6)", [
            "Incorporate Pvt. Ltd.; apply for Startup India Seed Fund Scheme (SISFS ₹20 Lakh).",
            "Integrate live Razorpay production escrow; onboard 50 verified circular designers."
        ]),
        ("Phase 3: South India Expansion (Months 7-9)", [
            "Expand logistics hub into Tirupur knitwear corridor.",
            "Reach break-even volume of 200 monthly active orders generating ₹65,000/mo net profit."
        ])
    ]
    for p_name, p_bullets in phases:
        p_t = tf_rm.add_paragraph()
        p_t.text = p_name
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_DARK
        p_t.space_before = Pt(8)
        for b in p_bullets:
            p_b = tf_rm.add_paragraph()
            p_b.text = "• " + b
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = TEXT_MUTED
            p_b.space_before = Pt(2)

    s11.notes_slide.notes_text_frame.text = (
        "Our prototype was built with strict fiscal discipline. A ₹50,000 budget covers hosting, field trials, swatch logistics, and DPIIT incorporation. "
        "With working software already demonstrated, our post-submission roadmap targets the Startup India Seed Fund Scheme to scale across 25 mills and achieve cash break-even by month 9."
    )

    # =========================================================================
    # SLIDE 12: ENVIRONMENTAL IMPACT & CONCLUSION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12, DARK_BG)

    # Top Header
    h_box = s12.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(1.0))
    tf_h = h_box.text_frame
    tf_h.word_wrap = True
    ph1 = tf_h.paragraphs[0]
    ph1.text = "CUTLOOP: CLOSING THE TEXTILE LOOP"
    ph1.font.size = Pt(13)
    ph1.font.bold = True
    ph1.font.color.rgb = MINT
    
    ph2 = tf_h.add_paragraph()
    ph2.text = "Environmental Impact & Academic Capstone Sign-Off"
    ph2.font.size = Pt(28)
    ph2.font.bold = True
    ph2.font.color.rgb = WHITE
    ph2.space_before = Pt(4)

    # 3 Impact Stat Cards
    impact_stats = [
        ("1.85 kg CO2e", "Carbon Emissions Avoided", "Per kg of cotton remnant diverted from municipal landfill hauling or open-air incinerators."),
        ("2,700 Liters", "Virgin Water Saved", "Per kg of fabric recirculated, displacing fresh agricultural crop irrigation requirements."),
        ("40% to 60%", "Creator Cost Savings", "Direct material cost reductions delivered to small artisan studios and zero-waste designers.")
    ]
    for i, (num, label, desc) in enumerate(impact_stats):
        c_left = Inches(0.8 + i * 3.9)
        add_card(s12, c_left, Inches(1.8), Inches(3.7), Inches(2.2), DARK_CARD, MINT)
        tb = s12.shapes.add_textbox(c_left + Inches(0.2), Inches(1.95), Inches(3.3), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p_n = tf.paragraphs[0]
        p_n.text = num
        p_n.font.size = Pt(28)
        p_n.font.bold = True
        p_n.font.color.rgb = MINT

        p_l = tf.add_paragraph()
        p_l.text = label
        p_l.font.size = Pt(12)
        p_l.font.bold = True
        p_l.font.color.rgb = WHITE
        p_l.space_before = Pt(2)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_LIGHT
        p_d.space_before = Pt(4)

    # Bottom Verified Deliverables Box
    add_card(s12, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.5), DARK_CARD, AMBER)
    tb_bot = s12.shapes.add_textbox(Inches(1.1), Inches(4.45), Inches(11.1), Inches(2.2))
    tf_b = tb_bot.text_frame
    tf_b.word_wrap = True
    pb_t = tf_b.paragraphs[0]
    pb_t.text = "Complete Academic Deliverables Verified on Disk:"
    pb_t.font.size = Pt(15)
    pb_t.font.bold = True
    pb_t.font.color.rgb = AMBER

    deliverable_bullets = [
        "10 Working Microservice REST Endpoints across Spring Boot (8080) and FastAPI (8000).",
        "4 Verified Machine Learning & Deep Learning Models saved on disk in cutloop_ds/saved_models/.",
        "Model B MobileNetV2 (86.39%) vs Custom CNN (72.19%) baseline evaluation with Grad-CAM.",
        "Model A Balanced Random Forest (88.15%) and Model C K-Means (k=5, Silhouette 0.6686).",
        "Live Production Cloudflare Deployment verified mobile-responsive with zero CSS dropouts."
    ]
    for b in deliverable_bullets:
        p = tf_b.add_paragraph()
        p.text = "✓ " + b
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_before = Pt(4)

    s12.notes_slide.notes_text_frame.text = (
        "In conclusion, CUTLOOP is not just an academic exercise—it is a working technological solution to a multi-billion-dollar environmental challenge. "
        "Every kilogram of fabric we recirculate saves 2,700 liters of water and keeps carbon in circulation. "
        "We have fulfilled every requirement across Java, Data Science, Deep Learning, and Business Strategy with verified code and live endpoints. "
        "Thank you, and we welcome your questions."
    )

    # Save to disk
    out_path = r"c:\Users\dhruv\OneDrive\Desktop\ds\CUTLOOP\CUTLOOP_PRESENTATION_DECK.pptx"
    prs.save(out_path)
    
    sub_path = r"c:\Users\dhruv\OneDrive\Desktop\ds\CUTLOOP\submission\CUTLOOP_PRESENTATION_DECK.pptx"
    prs.save(sub_path)
    
    print(f"[✓] Successfully generated PPTX presentation at:\n  {out_path}\n  {sub_path}")
    print(f"Total Slides: {len(prs.slides)}")

if __name__ == "__main__":
    create_deck()
