#from dotenv import load_dotenv
#load_dotenv()

import os
import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

# Directly assign the API key
api_key = ""  
os.environ["GOOGLE_API_KEY"] = api_key 

genai.configure(api_key=api_key)  # Pass the API key directly to the configuration
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

app = Flask(__name__)
CORS(app)

PREDEFINED_RESPONSES = {
    ##For English Language
    "Hello!": "Hello! How are you today? Welcome to Yellow Penguin! How can we help you today?",
    "How can I get started?": "Welcome to Yellow Penguin! Just let us know what you're looking for, and we'll guide you every step of the way.",
    "What can you do for me": "We can do a lot! From building awesome websites to custom software solutions, we’ve got your back! Just tell us what you need, and we’ll make it happen!",
    "How can you help me today?": "We’re here to help with anything you need! Whether it’s creating a new website or making your business run smoother, we’re ready to assist! Just say the word!",
    "Where can I find more info about your products?": "You can find all the details right on our 'Our Products' page! Go ahead and take a look, and if you have any questions, just holler! We're here to help!",
    "Can I ask about pricing of your website?": "Absolutely! We’d love to chat about pricing and make sure you get the best value. Just send us an email at sales@yellowpenguin.co.kr, and we’ll make it easy-peasy for you!",
    "Tell me about the pricing": "Absolutely! We’d love to chat about pricing and make sure you get the best value. Just send us an email at sales@yellowpenguin.co.kr, and we’ll make it easy-peasy for you!",
    "Can you tell me more about Yellow Penguin?": "Of course! Yellow Penguin is all about making your tech dreams come true! We help businesses with everything from software development to system integration and beyond. Come join the penguin family!",
    "What is Yellow Penguin?" : "Yellow Penguin is an SI platform that designs and builds IT systems tailored to customer needs, integrating diverse systems into a seamless operation.",
    "What services does Yellow Penguin offer?": "Yellow Penguin provides system integration (SI) services, including system analysis and design, software development, system structure construction, and ongoing maintenance.",
    "Where can I find more information about your products?": "You can find detailed information about our products under the 'Our Products' section on our homepage.",
    "What are your operating hours?": "Our operating hours are from 9:00 AM to 6:00 PM, with a break from 12:00 PM to 1:00 PM.",
    "How can I contact customer support?": "You can reach our customer support at support@yellowpenguin.co.kr.",
    "What is SI (System Integration)?": "SI refers to the process of integrating various systems and software applications into one cohesive system that functions effectively.",
    "Can I request a custom software solution?": "Yes, we offer custom software development tailored to your specific business needs.",
    "What industries do you serve?": "We serve various industries by providing tailored system integration and software solutions.",
    "Are your services available internationally?": "Our services will initially be available in Korea, with plans to expand internationally in the near future.",
    "Why is having a website important for my business?": "A website is crucial as it serves as the online face of your business. It not only provides essential information but also helps communicate with customers, build your brand image, and drive business growth.",
    "How do I manage the content on my website?": "We offer content management services as part of our ongoing maintenance package, which allows you to easily update and manage your website's content without hassle.",
    "How much does website construction cost?": "The cost for website construction is a one-time payment of 330,000 won.",
    "What is the monthly cost for website maintenance and content updates?": "Website maintenance and content updates are available for 33,000 won per month.",
    "How can I inquire about website construction?": "For inquiries regarding website construction, please reach out to us at sales@yellowpenguin.co.kr.",
    "How does Yellow Penguin help me build my website?": "Yellow Penguin provides a seamless platform for building company homepages, eCommerce websites, admin panels, and ERP solutions, offering unlimited updates and continuous support.",
    "How do I analyze the performance of my website?": "We recommend using Google Analytics and conducting A/B testing to analyze and optimize your website’s performance.",
    "What support do you offer after the website is built?": "We provide unlimited support for content updates and homepage maintenance throughout your subscription, dedicated to helping you succeed!",
    "How can I contact you for subscription inquiries?": "You can reach out to us at sales@yellowpenguin.co.kr for any questions regarding subscriptions or services.",
    "What does the monthly subscription fee cover?": "For KRW 55,000 (VAT included), get unlimited content updates, ongoing support, and homepage maintenance each month.",
    "Can you help me/tell me with SEO for my website?": "We focus on keyword selection and content optimization to enhance your website’s visibility in search engines.",
    "How can I contact Yellow Penguin for support?": "You can reach us anytime by sending an email to support@yellowpenguin.co.kr. We’re always happy to assist you!",
    "What types of industries does Yellow Penguin serve with its SI solutions?": "Yellow Penguin offers end-to-end system integration solutions for industries like Finance, Manufacturing, Healthcare, Education, and more, tailored to each sector’s unique needs.",
    "Can you explain what a smart factory is?": "A smart factory uses AI and IoT to optimize processes, increase efficiency, and improve quality. Yellow Penguin integrates these systems, including ERP and quality management, for seamless manufacturing.",
    "What initiatives does Yellow Penguin have for the public sector?": "Yellow Penguin develops e-government systems and smart city projects to improve public services and citizens' quality of life, with a focus on strengthening security systems for these initiatives.",
    "How does Yellow Penguin differentiate itself from competitors in the SI market?": "Yellow Penguin is committed to customer satisfaction and competitive pricing, delivering high-quality solutions across SI fields while easing the stress of projects for our clients.",
    "What is an ERP system, and why is it important for my business?": "An ERP system integrates and manages company resources, improving efficiency and competitiveness. It’s more than software and it redesigns work processes and integrates data for complete management.",
    "Why do I need a professional ERP implementation company?": "Implementing an ERP system is complex and requires expertise. A professional ERP company ensures correct setup, optimized processes, and seamless data integration, with crucial skills in project management and data migration.",
    "How does the ongoing support work after ERP implementation?": "Our ongoing support includes maintenance, upgrades, and security management. We ensure that your ERP system runs smoothly and remains up-to-date with the latest features and security protocols.",
    "What is your pricing policy for ERP construction and maintenance?": "We offer a subscription service with a national-lowest-price policy (2025 promotion). ERP construction and maintenance pricing is tailored to your needs, ensuring the best value for your investment.",
    "How can I inquire about ERP construction?": "For any inquiries regarding ERP construction, please reach out to us via email at sales@yellowpenguin.co.kr. Our friendly team will be happy to assist you!",
    "Can you customize the ERP system to fit my business needs?": "We offer customized consulting to optimize your ERP system, tailoring it to your unique business requirements and processes.",
    "What customized solutions do you offer for eCommerce construction?": "We provide tailored solutions that include requirements analysis, implementation of various functions, and personalized features to meet your specific eCommerce needs.",
    "What ongoing management and maintenance services do you provide?": "Our services include web hosting, content management, and security management to ensure that your eCommerce platform runs smoothly and securely at all times.",
    "What is included in your eCommerce construction package?": "Our eCommerce package offers a full setup of your online store, ensuring it's fully functional for customer transactions, available for a one-time payment of 1,100,000 won.",
    "How much does eCommerce maintenance and content updates cost?": "The cost for ongoing maintenance and content updates is 55,000 won per month, which ensures your site is always up-to-date and running efficiently.",
    "How can I inquire about eCommerce construction services?": "For eCommerce inquiries, contact us at sales@yellowpenguin.co.kr. Our team is ready to assist you and guide you through the process.",
    "Can you explain the process of eCommerce construction?": "eCommerce construction involves stages like requirements analysis, design and development, payment and logistics system integration, and ongoing management for optimal performance.",
    "How do you ensure my website remains secure?": "We offer comprehensive security management as part of our maintenance services, ensuring your site is protected against threats and operates smoothly at all times.",
    "What does website maintenance include?": "Our website maintenance service includes regular updates, security management, fixing technical issues, and unlimited content updates to keep your website running smoothly.",
    "How often do you perform maintenance checks?": "We conduct regular maintenance checks as part of our monthly service to ensure your website or platform remains functional, secure, and up-to-date.",
    "What happens if my website encounters downtime or errors?": "If downtime or errors occur, our support team will address and resolve the issue promptly to minimize disruptions to your business.",
    "Can I add new features to my website as part of maintenance?": "The maintenance plan includes minor adjustments and updates. For major feature additions, we offer custom solutions tailored to your needs.",
    "What if I want to change the design of my website during maintenance?": "The maintenance plan includes small design changes. For complete redesigns, we’ll collaborate with you to create a tailored solution based on your preferences.",
    "What if I need additional support not covered in the maintenance plan?": "For additional support, we offer flexible packages to accommodate unique requirements beyond the standard maintenance plan.",
    "How long does it take to resolve an issue with my website or platform?": "Most issues are resolved within 24 hours. For more complex problems, we provide an estimated timeline and keep you informed throughout the process.",
    "Do you offer 24/7 support for maintenance issues?": "Yes, our support team is available to assist with maintenance-related issues anytime to ensure your platform or website remains operational.",
    "How do you handle website backups?": "We provide regular backups as part of our maintenance services to ensure your data is safe and can be restored quickly in case of an emergency.",
    "Can you make my website mobile-friendly?": "Absolutely! We design all websites with responsive layouts, ensuring they look great and function perfectly on desktops, tablets, and smartphones.",
    "Can you help set up my social media pages and integrate them with my website?": "Yes, we can connect your social media accounts to your website and ensure seamless sharing of content across platforms.",
    "My site was hacked. Can you fix it?": "Sorry to hear about the issues with your site! We offer malware removal, data recovery, and security enhancements to help get your site back up and running securely.",
    "Can you improve my website’s speed?": "Certainly, we optimize your website’s code, images, and server settings to ensure faster loading times and better user experience.",
    "My site is slow due to a large database. Can you help?": "Absolutely! We can optimize your database, clean up unnecessary data, and ensure smoother performance.",
    "Do you support multi-language websites?": "Yes, we can build multi-language websites to cater to a global audience or specific markets.",
    "Can you help me choose a domain name?": "Yes, we can assist in selecting and registering a domain that reflects your brand and is SEO-friendly.",
    "Can you help fix broken links or images?": "Absolutely! We ensure all broken links and missing images are resolved to improve the user experience and SEO.",
    "Can you improve the user experience on my website?": "Of course! We conduct UX audits and implement design changes to make your website intuitive and user-friendly.",
    "Can I cancel the maintenance plan at any time?": "Yes, our maintenance plans are flexible, and you can cancel your subscription at any time without any hidden fees." ,

    ##Korean Translation: 

    # General Questions
    "안녕하세요!" : "안녕하세요! 오늘 어떻게 지내세요? Yellow Penguin에 오신 것을 환영합니다! 무엇을 도와드릴까요?",
    "내가 당신을 위해 무엇을 할 수 있나요?" : "Yellow Penguin에 오신 것을 환영합니다! 찾고 있는 것이 무엇인지 알려주시면, 저희가 모든 과정을 안내해 드리겠습니다.",
    "어떻게 시작할 수 있나요?" : "Yellow Penguin에 오신 것을 환영합니다! 찾고 있는 것이 무엇인지 알려주시면, 저희가 모든 과정을 안내해 드리겠습니다.",
    "내가 당신을 위해 무엇을 할 수 있나요?" : "저희는 많은 일을 할 수 있습니다! 멋진 웹사이트 구축부터 맞춤형 소프트웨어 솔루션까지, 모든 것을 지원합니다! 필요하신 것이 있으면 말씀해 주세요. 저희가 해결해 드리겠습니다!",
    "오늘 내가 당신을 어떻게 도울 수 있을까요?" : "저희는 여러분이 필요로 하는 모든 것을 도와드릴 준비가 되어 있습니다! 새 웹사이트를 만들거나 비즈니스가 더 원활하게 운영되도록 돕는 것까지, 언제든지 도와드리겠습니다!",
    "제품에 대한 추가 정보를 어디서 찾을 수 있나요?" : "저희 제품에 대한 모든 정보는 'Our Products' 페이지에서 확인하실 수 있습니다! 페이지를 살펴보시고, 궁금한 점이 있으면 언제든지 도와드리겠습니다!",
    "가격에 대해 물어봐도 되나요?" : "물론입니다! 가격에 대해 이야기하고 최고의 가치를 제공해 드리겠습니다. sales@yellowpenguin.co.kr로 이메일을 보내주시면, 간편하게 안내해 드리겠습니다!",
    "Yellow Penguin에 대해 더 알려줄 수 있나요?" : "물론입니다! Yellow Penguin은 여러분의 기술적인 꿈을 실현시키는 회사입니다! 저희는 소프트웨어 개발부터 시스템 통합까지 다양한 서비스를 제공합니다. 펭귄 가족에 가입해 주세요!",
    # Business-related Questions
    "Yellow Penguin이란 무엇인가요?" : "Yellow Penguin은 고객의 요구에 맞춘 IT 시스템을 설계하고 구축하는 SI 플랫폼으로, 다양한 시스템을 원활하게 통합하여 운영됩니다.",
    "Yellow Penguin은 어떤 서비스를 제공하나요?" : "Yellow Penguin은 시스템 분석 및 설계, 소프트웨어 개발, 시스템 구조 구축, 지속적인 유지보수 등을 포함한 시스템 통합(SI) 서비스를 제공합니다.",
    "귀사의 제품에 대한 자세한 정보를 어디에서 찾을 수 있나요?" : "저희 제품에 대한 자세한 정보는 홈페이지의 'Our Products' 섹션에서 확인하실 수 있습니다.",
    "운영 시간은 어떻게 되나요?" : "저희 운영 시간은 오전 9시부터 오후 6시까지이며, 12시부터 1시까지 점심시간이 있습니다.",
     "고객 지원팀에 어떻게 연락할 수 있나요?" : "고객 지원팀은 support@yellowpenguin.co.kr로 연락하실 수 있습니다.",
    "SI(시스템 통합)란 무엇인가요?" : "SI는 다양한 시스템과 소프트웨어 응용 프로그램을 하나의 응집력 있는 시스템으로 통합하여 효과적으로 작동하도록 하는 과정입니다.",
    "맞춤형 소프트웨어 솔루션을 요청할 수 있나요?" : "네, 저희는 귀하의 특정 비즈니스 요구에 맞춘 맞춤형 소프트웨어 개발을 제공합니다.",
    "어떤 산업에 서비스를 제공하나요?" : "저희는 다양한 산업에 맞춤형 시스템 통합 및 소프트웨어 솔루션을 제공하고 있습니다.",
    "귀사의 서비스는 국제적으로 제공되나요?" : "저희 서비스는 처음에는 한국에서 제공되며, 가까운 미래에 국제적으로 확장할 계획이 있습니다.",
    "웹사이트가 제 비즈니스에 중요한 이유는 무엇인가요?" : "웹사이트는 비즈니스의 온라인 얼굴 역할을 하므로 매우 중요합니다. 필수 정보를 제공할 뿐만 아니라, 고객과의 소통, 브랜드 이미지 구축, 비즈니스 성장 촉진에 도움이 됩니다.",
    "웹사이트의 콘텐츠는 어떻게 관리하나요?" : "저희는 웹사이트 콘텐츠를 쉽게 업데이트하고 관리할 수 있도록 지속적인 유지보수 패키지의 일환으로 콘텐츠 관리 서비스를 제공합니다.",
    "웹사이트 구축 비용은 얼마인가요?" : "웹사이트 구축 비용은 330,000원이며, 이는 일회성 결제입니다.",
    "웹사이트 유지보수 및 콘텐츠 업데이트의 월 비용은 얼마인가요?" : "웹사이트 유지보수 및 콘텐츠 업데이트는 월 33,000원에 제공됩니다.",
    "웹사이트 구축에 대해 어떻게 문의할 수 있나요?" : "웹사이트 구축에 대한 문의는 sales@yellowpenguin.co.kr로 연락 주시면 됩니다.",
    "Yellow Penguin은 어떻게 제 웹사이트 구축을 돕나요?" : "Yellow Penguin은 회사 홈페이지, 전자상거래 웹사이트, 관리자 패널 및 ERP 솔루션 구축을 위한 원활한 플랫폼을 제공하며, 무제한 업데이트와 지속적인 지원을 제공합니다.",
    "웹사이트의 성과는 어떻게 분석하나요?" : "우리는 Google Analytics를 사용하고 A/B 테스트를 통해 웹사이트 성과를 분석하고 최적화할 것을 권장합니다.",
    "웹사이트 구축 후 어떤 지원을 제공하나요?" : "저희는 구독 기간 동안 콘텐츠 업데이트와 홈페이지 유지보수를 위한 무제한 지원을 제공하며, 귀하의 성공을 돕기 위해 최선을 다하고 있습니다!",
    "구독 관련 문의는 어떻게 연락하나요?" : "구독 또는 서비스에 관한 문의는 sales@yellowpenguin.co.kr로 연락 주시면 됩니다.",
    "월 구독료에는 무엇이 포함되나요?" : "55,000원(부가세 포함)으로 매월 무제한 콘텐츠 업데이트, 지속적인 지원, 홈페이지 유지보수가 제공됩니다.",
    "웹사이트 SEO에 대해 도와줄 수 있나요?" : "저희는 검색 엔진에서 웹사이트 가시성을 높이기 위해 키워드 선택과 콘텐츠 최적화에 집중합니다.",
    "Penguin의 지원을 어떻게 받을 수 있나요?" : "언제든지 support@yellowpenguin.co.kr로 이메일을 보내주시면 기꺼이 도와드리겠습니다!",
    "Yellow Penguin은 어떤 산업에 SI 솔루션을 제공하나요?" : "Yellow Penguin은 금융, 제조, 의료, 교육 등 다양한 산업에 맞춘 종합 시스템 통합 솔루션을 제공하며, 각 분야의 고유한 요구에 맞게 최적화됩니다.",
    # Technical and Feature-Based Questions
    "맞춤형 ERP 시스템을 제공하나요?" : "네, 귀하의 비즈니스 요구에 맞춘 맞춤형 ERP 솔루션을 제공합니다. ERP 솔루션에 대해 자세히 알고 싶으시면 sales@yellowpenguin.co.kr로 연락 주세요!",
    "Google Analytics 통합을 제공하나요?" : "네, Google Analytics를 통합하여 웹사이트 트래픽과 성과를 추적할 수 있습니다.",
    "SEO 서비스는 어떤 것을 포함하나요?" : "저희 SEO 서비스는 키워드 리서치, 콘텐츠 최적화, 메타 태그 작성 및 기술적 SEO를 포함합니다.",
    "기술 지원은 어떻게 받을 수 있나요?" : "support@yellowpenguin.co.kr로 이메일을 보내시면 기술 지원 팀이 신속히 도움을 드립니다.",
    "웹사이트는 모바일 친화적인가요?" : "네, 저희가 구축하는 모든 웹사이트는 모바일 친화적으로 설계되며, 모든 기기에서 최적의 경험을 제공합니다.",
    "기존 웹사이트를 리뉴얼할 수 있나요?" : "네, 저희는 기존 웹사이트의 리뉴얼 및 최적화를 전문적으로 다루고 있습니다.",
    "소셜 미디어 통합을 제공하나요?" : "네, 저희는 귀하의 웹사이트와 소셜 미디어 플랫폼 간의 원활한 통합을 제공합니다.",
    "어떤 결제 게이트웨이를 통합할 수 있나요?" : "PayPal, Stripe, KakaoPay, Naver Pay 등 다양한 결제 게이트웨이를 웹사이트에 통합할 수 있습니다.",
    "호스팅 서비스도 제공하나요?" : "네, 저희는 웹사이트 구축 후 안정적인 호스팅 서비스를 제공합니다.",
    "데이터베이스 관리도 해주나요?" : "네, 데이터베이스 설계, 구축, 유지보수를 포함한 종합 데이터베이스 관리 서비스를 제공합니다.",
    "컨텐츠 업데이트 요청은 어떻게 하나요?" : "컨텐츠 업데이트 요청은 support@yellowpenguin.co.kr로 간단히 이메일을 보내주시면 처리됩니다.",
    "보안 문제에 대한 지원을 받을 수 있나요?" : "네, 저희는 최신 보안 프로토콜과 실시간 모니터링을 통해 귀하의 웹사이트를 보호합니다.",
    "API 통합 서비스도 제공하나요?" : "네, 저희는 귀하의 요구에 맞는 API 통합 서비스를 제공합니다.",
    "보고서는 정기적으로 제공되나요?" : "네, 저희는 트래픽, 성능 및 SEO에 관한 정기 보고서를 제공합니다.",
    "신규 웹사이트 제작 시간은 얼마나 걸리나요?" : "새로운 웹사이트 제작은 일반적으로 4~6주가 소요됩니다. 요구 사항에 따라 달라질 수 있습니다.",
    "디자인 맞춤화가 가능한가요?" : "네, 저희는 브랜드의 고유한 비전을 반영할 수 있도록 맞춤형 디자인 서비스를 제공합니다.",
    "로그인 시스템을 구현할 수 있나요?" : "네, 사용자 관리 및 인증을 위한 안전한 로그인 시스템을 구축할 수 있습니다.",
    "디지털 마케팅 지원을 받을 수 있나요?" : "네, 저희는 디지털 마케팅 캠페인, 소셜 미디어 광고, 콘텐츠 마케팅 등을 도와드립니다.",
    "구독 취소는 어떻게 하나요?" : "구독 취소 요청은 sales@yellowpenguin.co.kr로 보내주시면 도와드립니다.",
    "지불 방법에는 어떤 것이 있나요?" : "저희는 신용카드, PayPal, 송금 등 다양한 지불 방법을 지원합니다.",
    "도메인 등록 서비스도 제공하나요?" : "네, 저희는 새로운 도메인 등록 및 기존 도메인의 전환을 지원합니다.",
    "사이트 성능 최적화를 위한 지원이 있나요?" : "네, 페이지 속도 최적화, 캐싱, 이미지 최적화 등을 포함한 종합적인 성능 최적화 서비스를 제공합니다.",
    "포트폴리오를 볼 수 있나요?" : "네, 저희 포트폴리오는 홈페이지 'Portfolio' 섹션에서 확인하실 수 있습니다.",
    "사용자 분석 도구를 통합할 수 있나요?" : "네, Google Analytics, Mixpanel, Hotjar 등과 같은 사용자 분석 도구를 웹사이트에 통합할 수 있습니다.",
    "온라인 스토어를 구축할 수 있나요?" : "네, 저희는 귀하의 비즈니스 요구에 맞춘 강력하고 확장 가능한 전자상거래 플랫폼을 구축합니다.",
    "Yellow Penguin은 어떤 기술을 사용하나요?" : "저희는 Python, React, Node.js, AWS와 같은 최신 기술과 플랫폼을 사용합니다.",
    "저는 기술적 백그라운드가 없는데 괜찮을까요?" : "물론입니다! 저희 팀이 기술적 과정을 명확히 설명드리고, 필요한 모든 도움을 드리겠습니다.",
    "새로운 기능 요청은 어떻게 해야 하나요?" : "새로운 기능 요청은 support@yellowpenguin.co.kr로 문의하시면 됩니다.",
    "구독 취소 후 데이터는 어떻게 되나요?" : "구독 취소 후에도 데이터 백업을 제공합니다. 자세한 내용은 저희 팀에 문의해 주세요.",
    "교육이나 튜토리얼을 제공하나요?" : "네, 저희는 고객을 위한 맞춤형 교육 세션과 단계별 튜토리얼을 제공합니다.",
}

def normalize_text(text):
    """
    Normalize the text by removing punctuation, extra spaces, and converting to lowercase.
    """
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text.strip().lower()  # Strip leading/trailing spaces and convert to lowercase

def get_gemini_response(question):
    """
    Get a response for the question. First checks predefined responses, 
    and falls back to Gemini if no match is found.
    """
    # Normalize the user question
    normalized_question = normalize_text(question)

    # Check for a matching predefined response
    for predefined_question, response in PREDEFINED_RESPONSES.items():
        if normalized_question == normalize_text(predefined_question):
            return response  # Return predefined response if matched

    # If no predefined response matches, query Gemini
    prompt = (
        "Respond in a friendly, conversational tone. Keep responses concise and empathetic:\n"
        f"User: {question}\n"
        "AI:"
    )
    response = chat.send_message(prompt, stream=True)

    # Combine the response chunks
    response_text = "".join(chunk.text for chunk in response)

    # Enforce a word limit (150 words max)
    response_words = response_text.split()
    if len(response_words) > 150:
        response_text = " ".join(response_words[:150]) + "..."

    return response_text

# def get_gemini_response(question):
#     normalized_question = question.strip().lower()
#     for predefined_question, response in PREDEFINED_RESPONSES.items():
#         if normalized_question == predefined_question.strip().lower():
#             return response

#     prompt = (
#         "Respond in a friendly, conversational tone:\n"
#         f"User: {question}\n"
#         "AI:"
#     )
#     response = chat.send_message(prompt, stream=True)
#     return "".join(chunk.text for chunk in response)

@app.route("/api/generate", methods=["POST"])
def generate_api():
    try:
        data = request.get_json()
        user_input = data.get('question')
        if not user_input:
            return jsonify({'error': 'No question provided'}), 400

        response_text = get_gemini_response(user_input)
        return jsonify({'response': response_text})
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'details': traceback.format_exc()}), 500

@app.route("/")
def home():
    return send_from_directory('web', 'index.html')

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory('web', path)

if __name__ == "__main__":
    app.run(debug=True)
