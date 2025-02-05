from dotenv import load_dotenv
load_dotenv()
import json
import os
from fuzzywuzzy import fuzz
import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
#from difflib import get_close_matches #(for words to match)
#from langdetect import detect

# Directly assign the API key
api_key = ""  
os.environ["GOOGLE_API_KEY"] = api_key 

genai.configure(api_key=api_key)  # Pass the API key directly to the configuration
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

app = Flask(__name__)
CORS(app)

from functools import lru_cache
@lru_cache(maxsize=100)  # Cache up to 100 responses

def get_predefined_responses():
    return {
    ##For English Language
    "Hello!": "Hello! How are you today? Welcome to Yellow Penguin! How can we help you today?",
    "hi": "Hello! How are you today? Welcome to Yellow Penguin! How can we help you today?",
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
    "How much does website construction cost/price?": "The cost for website construction is a one-time payment of 330,000 won.",
    "How much does website building/creating cost/price?": "The cost for website building is a one-time payment of 330,000 won.",
    "What is the monthly cost for website maintenance and content updates?": "Website maintenance and content updates are available for 33,000 won per month.",
    "How can I inquire about website construction?": "For inquiries regarding website construction, please reach out to us at support@yellowpenguin.co.kr.",
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
    "How can I inquire about ERP construction?": "For any inquiries regarding ERP construction, please reach out to us via email at support@yellowpenguin.co.kr. Our friendly team will be happy to assist you!",
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

    #basic questions added:
    "I am new, how can you help me built a new website?": "Yellow Penguin provides a seamless platform for building company homepages, eCommerce websites, admin panels, and ERP solutions, offering unlimited updates and continuous support.",
    "I mean if you guys make a wesbite for me.. how much time it will take and what is the cost?": "For inquiries regarding website construction & time, please reach out to us at sales@yellowpenguin.co.kr.",
    "Time to build website?": "For inquiries regarding website construction & time, please reach out to us at support@yellowpenguin.co.kr.",
    "Cost to build website?": "For inquiries regarding website construction & time, please reach out to us at sales@yellowpenguin.co.kr.",
    "help" : "We’re here to help with anything you need! Whether it’s creating a new website or making your business run smoother, we’re ready to assist!",
    "cost" : "Absolutely! We’d love to chat about pricing and make sure you get the best value. Just send us an email at sales@yellowpenguin.co.kr.",
    "price" : "Absolutely! We’d love to chat about pricing and make sure you get the best value. Just send us an email at sales@yellowpenguin.co.kr.",
    "services" : "Yellow Penguin provides system integration (SI) services, including system analysis and design, software development, system structure construction, and ongoing maintenance.",
    "support" : "You can reach us anytime by sending an email to support@yellowpenguin.co.kr. We’re always happy to assist you!",
    "contact" : "You can reach out to us at support@yellowpenguin.co.kr. for any help",
    "contact you?" : "You can reach out to us at support@yellowpenguin.co.kr. for any help",
    "how to contact you": "You can reach out to us at support@yellowpenguin.co.kr. for any help.",
    "help me" : "We’re here to help with anything you need! Whether it’s creating a new website or making your business run smoother, we’re ready to assist!",
    "hello" : "Hello! How are you today? Welcome to Yellow Penguin! How can we help you today?",
    "what can you do for me": "We can do a lot! From building awesome websites to custom software solutions, we’ve got your back! Just tell us what you need, and we’ll make it happen!",
    "e-Commerce?": "We provide tailored solutions that include requirements analysis, implementation of various functions, and personalized features to meet your specific eCommerce needs",
    "e-Commerce time?": "For eCommerce inquiries, contact us at sales@yellowpenguin.co.kr. Our team is ready to assist you and guide you through the process.",
    "e-Commerce cost?": "For eCommerce inquiries, contact us at sales@yellowpenguin.co.kr.",
    "e-Commerce help?": "For eCommerce inquiries, contact us at sales@yellowpenguin.co.kr.",
    "e-Commerce support?": "For eCommerce inquiries, contact us at support@yellowpenguin.co.kr.",
    "e-Commerce contact?": "For eCommerce inquiries, contact us at sales@yellowpenguin.co.kr. Our team is ready to assist you and guide you through the process.",
    "e-Commerce help me?": "For eCommerce inquiries, contact us at sales@yellowpenguin.co.kr. Our team is ready to assist you and guide you through the process. ",
    "e-Commerce construction": "For eCommerce inquiries, contact us at sales@yellowpenguin.co.kr. Our team is ready to assist you and guide you through the process.For pricing or cost contact us at sales@yellowpenguin.co.kr.",
    "eCommerce ": "Hello, please be more specific with what you want to know from me about this. I will be happy to help!",
    "what products you guys offer?": "You can find all the details right on our 'Our Products' page! Go ahead and take a look, and if you have any questions. We're here to help!",
    "products": "You can find all the details right on our 'Our Products' page! Go ahead and take a look,and if you have any questions. We're here to help!",
    "products?": "You can find all the details right on our 'Our Products' page! Go ahead and take a look, and if you have any questions. We're here to help!",
    "products help": "You can find detailed information about our products under the 'Our Products' section on our homepage.",
    "products support": "You can find detailed information about our products under the 'Our Products' section on our homepage.",
    "products contact": "You can find detailed information about our products under the 'Our Products' section on our homepage. If you have any questions. We're here to help!",
    "let me know about your products": "You can find detailed information about our products under the 'Our Products' section on our homepage.",
    "products cost": "You can find detailed information about our products under the 'Our Products' section on our homepage. And for cost contact us at sales@yellowpenguin.co.kr.",
    "products price": "You can find detailed information about our products under the 'Our Products' section on our homepage. And for price contact us at sales@yellowpenguin.co.kr.",
    "products time": "You can find detailed information about our products under the 'Our Products' section on our homepage. And for time contact us at support@yellowpenguin.co.kr.",
    "products construction": "You can find detailed information about our products under the 'Our Products' section on our homepage. And for construction contact us at support@yellowpenguin.co.kr.",
    "products maintenance": "For additional support, we offer flexible packages to accommodate unique requirements beyond the standard maintenance plan. Ask me in more detail, so that I can help you with your desired product & its maintenance.",
    "products help me": "You can find detailed information about our products under the 'Our Products' section on our homepage.",
    "products hello": "You can find detailed information about our products under the 'Our Products' section on our homepage.",
    "products support me": "You can find detailed information about our products under the 'Our Products' section on our homepage. Or contact us for support at support@yellowpenguin.co.kr.",
    "website": "We provide a seamless platform for building company homepages, eCommerce websites, admin panels, and ERP solutions, offering unlimited updates and continuous support.",    
    "website?": "We provide a seamless platform for building company homepages, eCommerce websites, admin panels, and ERP solutions, offering unlimited updates and continuous support.",
    "website help": "From building awesome websites to custom software solutions, we’ve got your back! Just tell us what you need, and we’ll make it happen!We provide a seamless platform for building company homepages, eCommerce websites, admin panels, and ERP solutions, offering unlimited updates and continuous support.",
    "website support": "You can reach out to us at sales@yellowpenguin.co.kr.",
    "website contact": "You can reach out to us at sales@yellowpenguin.co.kr.",
    "website’s speed": "Certainly, we optimize your website’s code, images, and server settings to ensure faster loading times and better user experience.",
    "website hacked": "It would be great if you could be more specific with the issue you are facing with your website. Sorry to hear about the issues with your site! We offer malware removal, data recovery, and security enhancements to help get your site back up and running securely.",
    "website slow": "Absolutely! We can optimize your website’s code, images, and server settings to ensure faster loading times and better user experience. Contact us at sales@yellowpenguin.co.kr.",
    "website database": "Absolutely! We can optimize your database, clean up unnecessary data, and ensure smoother performance.",
    "website multi-language": "Yes, we can build multi-language websites to cater to a global audience or specific markets.",
    "website domain": "Yes, we can assist in selecting and registering a domain that reflects your brand and is SEO-friendly.",
    "website broken links": "Absolutely! We ensure all broken links and missing images are resolved to improve the user experience and SEO.",
    "website user experience": "Of course! We conduct UX audits and implement design changes to make your website intuitive and user-friendly.",
    "website cancel": "Yes, our maintenance plans are flexible, and you can cancel your subscription at any time without any hidden fees.",
    "website maintenance": "Our website maintenance service includes regular updates, security management, fixing technical issues, and unlimited content updates to keep your website running smoothly.",
    "website downtime": "If downtime or errors occur, our support team will address and resolve the issue promptly to minimize disruptions to your business.",
    "website backups": "We provide regular backups as part of our maintenance services to ensure your data is safe and can be restored quickly in case of an emergency.",
    "website additional support": "For additional support, we offer flexible packages to accommodate unique requirements beyond the standard maintenance plan.",
    "website resolve issue": "Most issues are resolved within 24 hours. For more complex problems, we provide an estimated timeline and keep you informed throughout the process.",
    "website 24/7 support": "Yes, our support team is available to assist with maintenance-related issues anytime to ensure your platform or website remains operational.",
    "website design": "The maintenance plan includes small design changes. For complete redesigns, we’ll collaborate with you to create a tailored solution based on your preferences.",
    "website redesign": "The maintenance plan includes small design changes. For complete redesigns, we’ll collaborate with you to create a tailored solution based on your preferences.",
    "website feature": "The maintenance plan includes minor adjustments and updates. For major feature additions, we offer custom solutions tailored to your needs.",
    #"website feature addition": "The maintenance plan includes minor adjustments and updates. For major feature additions, we offer custom solutions tailored to your needs.",
    "website management": "Our ongoing support includes maintenance, upgrades, and security management. We ensure that your website or platform runs smoothly and remains up-to-date with the latest features and security protocols.",
    "website management ongoing": "Our ongoing support includes maintenance, upgrades, and security management. We ensure that your website or platform runs smoothly and remains up-to-date with the latest features and security protocols.",
    "website cost" :"The cost for website construction is a one-time payment of 330,000 won.",
    "website management after": "Our ongoing support includes maintenance, upgrades, and security management. We ensure that your website or platform runs smoothly and remains up-to-date with the latest features and security protocols.",
    "website management after ERP": "Our ongoing support includes maintenance, upgrades, and security management. We ensure that your website or platform runs smoothly and remains up-to-date with the latest features and security protocols.",
    "website management ERP": "Our ongoing support includes maintenance, upgrades, and security management. We ensure that your website or platform runs smoothly and remains up-to-date with the latest features and security protocols.",
    "ERP system": "An ERP system integrates and manages company resources, improving efficiency and competitiveness. It’s more than software and it redesigns work processes and integrates data for complete management.",
    "maintenance plan": "Our maintenance plans are flexible, and you can cancel your subscription at any time without any hidden fees.",
    "maintenance plan cancel": "Our maintenance plans are flexible, and you can cancel your subscription at any time without any hidden fees.",
    "maintenance plan flexible": "Our maintenance plans are flexible, and you can cancel your subscription at any time without any hidden fees.",
    "maintenance plan additional": "For additional support, we offer flexible packages to accommodate unique requirements beyond the standard maintenance plan.",
    "SEO": "We focus on keyword selection and content optimization to enhance your website’s visibility in search engines.",
    "erp": "An ERP system integrates and manages company resources, improving efficiency and competitiveness. It’s more than software and it redesigns work processes and integrates data for complete management.",
    ##Korean Translation: 
    # General Questions
    "안녕": "안녕하세요! 오늘 어떻게 지내세요? 옐로우 펭귄에 오신 것을 환영합니다. 어떻게 도와드릴까요?",
    #"안녕": "안녕하세요! 오늘 어떻게 지내세요? 옐로우 펭귄에 오신 것을 환영합니다. 어떻게 도와드릴까요?",
    "안녕하세요!" : "안녕하세요! 오늘 어떻게 지내세요? Yellow Penguin에 오신 것을 환영합니다! 무엇을 도와드릴까요?",
    "내가 당신을 위해 무엇을 할 수 있나요?" : "Yellow Penguin에 오신 것을 환영합니다! 찾고 있는 것이 무엇인지 알려주시면, 저희가 모든 과정을 안내해 드리겠습니다.",
    "안녕하세요, 무엇을 해줄 수 있나요?" : "Yellow Penguin에 오신 것을 환영합니다! 찾고 있는 것이 무엇인지 알려주시면, 저희가 모든 과정을 안내해 드리겠습니다.",
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
    "웹사이트를 모바일 친화적으로 만들 수 있나요?" : "물론입니다! 저희는 모든 웹사이트를 반응형 레이아웃으로 디자인하여 데스크탑, 태블릿, 스마트폰에서 모두 잘 보이고 완벽하게 작동하도록 합니다.",
    "소셜 미디어 페이지를 설정하고 웹사이트와 통합하는 데 도움을 줄 수 있나요?" : " 네, 저희는 귀하의 소셜 미디어 계정을 웹사이트와 연결하여 다양한 플랫폼에서 콘텐츠가 원활하게 공유되도록 보장합니다.",
    "제 사이트가 해킹당했어요. 고칠 수 있나요?": "사이트 문제에 대해 듣게 되어 유감입니다! 저희는 악성 코드 제거, 데이터 복구, 보안 강화를 제공하여 사이트가 안전하게 다시 작동하도록 돕습니다.",
    "제 웹사이트의 속도를 개선할 수 있나요?" : "물론입니다, 저희는 웹사이트의 코드, 이미지, 서버 설정을 최적화하여 더 빠른 로딩 시간과 향상된 사용자 경험을 보장합니다.",
    "대형 데이터베이스로 인해 사이트가 느립니다. 도와줄 수 있나요?" : " 물론입니다! 저희는 데이터베이스 최적화, 불필요한 데이터 정리 등을 통해 더 원활한 성능을 보장합니다.",
    "다국어 웹사이트를 지원하나요?" : " 네, 저희는 글로벌 고객층이나 특정 시장을 겨냥한 다국어 웹사이트를 구축할 수 있습니다.",
    "도메인 이름을 선택하는 데 도움을 줄 수 있나요?" : " 네, 저희는 귀하의 브랜드를 반영하고 SEO에 최적화된 도메인을 선택하고 등록하는 데 도움을 드립니다.",
    "깨진 링크나 이미지를 고치는 데 도움을 줄 수 있나요?": "물론입니다! 저희는 모든 깨진 링크와 누락된 이미지를 해결하여 사용자 경험과 SEO를 개선합니다.",
    "웹사이트에서 사용자 경험을 개선할 수 있나요?" : "당연히요! 저희는 UX 감사 작업을 진행하고 디자인 변경을 구현하여 웹사이트가 직관적이고 사용자 친화적 있도록 만듭니다.",
    "유지보수 계획을 언제든지 취소할 수 있나요?" : "네, 저희의 유지보수 계획은 유연하며, 숨겨진 비용 없이 언제든지 구독을 취소하실 수 있습니다.",
    "웹사이트 다운타임이 발생하면 어떻게 대처하나요?" : "다운타임이나 오류가 발생하면 저희 지원팀이 문제를 신속히 해결하여 비즈니스에 최소한의 방해가 되도록 합니다. support@yellowpenguin.co.kr로 문의해주세요.",
    "정기적인 백업 서비스를 제공하나요?" : "저희는 비상 시를 대비하여 정기적인 백업 서비스를 제공하며, 데이터가 안전하게 보관되고 긴급 상황에서 빠르게 복구될 수 있도록 합니다.",
    "웹사이트 백업은 어떻게 처리하나요?": "저희는 유지보수 서비스의 일환으로 정기적인 백업을 제공하여 데이터를 안전하게 보호하고, 비상 시 신속하게 복구할 수 있도록 합니다.",
    "유지보수 문제에 대해 24/7 지원을 제공하나요?" : "네, 저희 지원팀은 유지보수 관련 문제에 대해 언제든지 지원을 제공하여 귀하의 플랫폼이나 웹사이트가 정상적으로 운영될 수 있도록 보장합니다",
    "웹사이트나 플랫폼에서 발생한 문제 해결은 얼마나 걸리나요?": "대부분의 문제는 24시간 이내에 해결됩니다. 복잡한 문제의 경우, 예상 소요 시간과 진행 상황에 대해 지속적으로 정보를 제공하며 해결을 지원합니다.",
    "유지보수 계획에 포함되지 않은 추가 지원이 필요하면 어떻게 하나요?" : "추가 지원이 필요한 경우, 표준 유지보수 계획을 넘어서는 요구 사항에 맞춘 유연한 패키지를 제공합니다.",
    "유지보수 중에 웹사이트 디자인을 변경하고 싶다면 어떻게 하나요?" : "유지보수 계획에는 소규모 디자인 변경이 포함됩니다. 전체적인 디자인 변경이 필요할 경우, 귀하의 취향에 맞춘 맞춤형 솔루션을 함께 협력하여 만들겠습니다.",
    "유지보수의 일환으로 웹사이트에 새로운 기능을 추가할 수 있나요?": "유지보수 계획에는 소규모 수정 및 업데이트가 포함됩니다. 주요 기능 추가가 필요한 경우, 귀하의 요구에 맞춘 맞춤형 솔루션을 제공합니다.",
    "웹사이트가 다운되거나 오류가 발생하면 어떻게 되나요?": "다운타임이나 오류가 발생하면 저희 지원팀이 신속하게 문제를 해결하여 비즈니스에 미치는 영향을 최소화합니다.",
    "유지보수 계획에 대한 자세한 정보를 어디서 확인할 수 있나요?" : "support@yellowpenguin.co.kr로 문의해주세요.",
    "유지보수 점검은 얼마나 자주 하나요?": "저희는 월간 서비스의 일환으로 정기적인 유지보수 점검을 실시하여 웹사이트나 플랫폼이 기능적이고 안전하며 최신 상태로 유지되도록 합니다.",
    "웹사이트 유지보수는 무엇을 포함하나요?" : "저희 웹사이트 유지보수 서비스는 정기적인 업데이트, 보안 관리, 기술적 문제 해결 및 무제한 콘텐츠 업데이트를 포함하여 웹사이트가 원활하게 운영되도록 보장합니다.",
    "웹사이트의 보안을 어떻게 유지하나요?" : "저희는 유지보수 서비스의 일환으로 포괄적인 보안 관리를 제공하여 웹사이트가 위협으로부터 보호되고 항상 원활하게 운영되도록 보장합니다.",
    "e-Commerce 구축 과정에 대해 설명해 주실 수 있나요?": "e-Commerce 구축은 요구사항 분석, 디자인 및 개발, 결제 및 물류 시스템 통합, 그리고 최적의 성능을 위한 지속적인 관리 단계로 진행됩니다.",
    "e-Commerce 구축 서비스에 대해 어떻게 문의할 수 있나요?" : "eCommerce 문의는 sales@yellowpenguin.co.kr로 연락주세요. 저희 팀이 기꺼이 도와드리며, 절차를",
    "eCommerce 유지보수 및 콘텐츠 업데이트 비용은 얼마인가요?" : "지속적인 유지보수 및 콘텐츠 업데이트 비용은 월 55,000원으로, 사이트가 항상 최신 상태로 효율적으로 운영되도록 보장합니다.",
    "eCommerce 구축 패키지에는 무엇이 포함되나요?" : "저희 eCommerce 패키지는 온라인 상점의 전체 설치를 제공하며, 고객 거래가 원활하게 이루어질 수 있도록 보장합니다. 이는 1,100,000원의 일회성 결제로 제공됩니다.",
    "지속적인 관리 및 유지보수 서비스는 무엇을 제공하나요?" : "저희 서비스에는 웹 호스팅, 콘텐츠 관리, 보안 관리가 포함되어 eCommerce 플랫폼이 항상 원활하고 안전하게 운영되도록 보장합니다.",
    "eCommerce 구축을 위한 맞춤형 솔루션은 무엇인가요?" : "저희는 요구 사항 분석, 다양한 기능 구현, 맞춤형 기능을 포함한 솔루션을 제공하여 고객님의 특정 eCommerce 요구를 충족시킵니다.",
    "ERP 시스템을 제 비즈니스 요구에 맞게 맞춤화할 수 있나요?" : "저희는 비즈니스 요구와 프로세스에 맞게 ERP 시스템을 최적화하는 맞춤형 컨설팅 서비스를 제공합니다.",
    "ERP 구축에 대해 어떻게 문의할 수 있나요?":"ERP 구축에 대한 문의는 sales@yellowpenguin.co.kr로 이메일을 보내주시면 됩니다. 저희 친절한 팀이 기꺼이 도와드리겠습니다!",
    "ERP 구축 및 유지보수에 대한 가격 정책은 무엇인가요?" : "저희는 국가 최저가 정책(2025 프로모션)을 기반으로 구독 서비스를 제공합니다. ERP 구축 및 유지보수 가격은 고객의 요구에 맞춰 조정되며, 투자에 대한 최상의 가치를 제공합니다.",
    "ERP 구현 후 지속적인 지원은 어떻게 이루어지나요?" : "저희의 지속적인 지원에는 유지보수, 업그레이드, 보안 관리가 포함됩니다. ERP 시스템이 원활하게 운영되며 최신 기능과 보안 프로토콜을 유지하도록 보장합니다.",
    "왜 전문 ERP 구현 회사가 필요하나요?":"ERP 시스템 구현은 복잡하며 전문적인 지식이 필요합니다. 전문 ERP 회사는 올바른 설정, 최적화된 프로세스, 원활한 데이터 통합을 보장하며, 프로젝트 관리 및 데이터 마이그레이션에 중요한 기술을 갖추고 있습니다.",
    "ERP 시스템이란 무엇이며, 제 비즈니스에 왜 중요한가요?": "ERP 시스템은 회사 자원을 통합하고 관리하여 효율성과 경쟁력을 향상시킵니다. 이는 단순한 소프트웨어가 아니라 업무 프로세스를 재설계하고 데이터를 통합하여 완전한 관리를 제공합니다.",
    "Yellow Penguin은 SI 시장에서 경쟁자들과 어떻게 차별화되나요?": "Yellow Penguin은 고객 만족과 경쟁력 있는 가격을 최우선으로, SI 분야에서 고품질 솔루션을 제공하며, 고객이 프로젝트에서 겪는 스트레스를 덜어주는 데 중점을 두고 있습니다.",
    "Yellow Penguin은 공공 부문을 위한 어떤 계획을 가지고 있나요?" : "Yellow Penguin은 전자 정부 시스템과 스마트 시티 프로젝트를 개발하여 공공 서비스와 시민들의 삶의 질을 향상시키며, 이들 프로젝트의 보안 시스템 강화를 중점적으로 추진하고 있습니다.",
    "스마트 팩토리가 무엇인가요?": "스마트 팩토리는 AI와 IoT를 활용하여 프로세스를 최적화하고 효율성을 높이며 품질을 향상시킵니다. Yellow Penguin은 ERP 및 품질 관리 시스템을 포함한 이러한 시스템을 통합하여 원활한 제조를 지원합니다.",
    "의료 분야에 대한 SI 솔루션은 어떤 것이 있나요?": "Yellow Penguin은 의료 분야에 맞춘 종합적인 SI 솔루션을 제공하며, 환자 관리, 의료 기록 시스템, 의료 장비 관리 등 다양한 서비스를 제공합니다.",
    " 월 구독료에는 무엇이 포함되나요?": "55,000원(부가세 포함)으로 매월 무제한 콘텐츠 업데이트, 지속적인 지원, 홈페이지 유지보수가 제공됩니다.",
    "구독 관련 문의는 어떻게 연락하나요?" : "구독 또는 서비스에 관한 문의는 sales@yellowpenguin.co.kr로 연락 주시면 됩니다.",
    "웹사이트 구축 후 어떤 지원을 제공하나요?": "저희는 구독 기간 동안 콘텐츠 업데이트와 홈페이지 유지보수를 위한 무제한 지원을 제공하며, 귀하의 성공을 돕기 위해 최선을 다하고 있습니다!",
    "웹사이트의 성과는 어떻게 분석하나요?": "우리는 Google Analytics를 사용하고 A/B 테스트를 통해 웹사이트 성과를 분석하고 최적화할 것을 권장합니다.",
    "SEO 서비스는 어떤 것을 포함하나요?": "저희는 검색 엔진에서 웹사이트 가시성을 높이기 위해 키워드 선택과 콘텐츠 최적화에 집중합니다.",
    "Penguin의 지원을 어떻게 받을 수 있나요?" : "support@yellowpenguin.co.kr로 문의해주세요.",
    "안녕하세요, 어떻게 시작할 수 있나요?": "Yellow Penguin에 오신 것을 환영합니다! 찾고 있는 것이 무엇인지 알려주시면, 저희가 모든 과정을 안내해 드리겠습니다.",
    "안녕하세요, 오늘 무엇을 도와줄 수 있나요?" : "저희는 여러분이 필요로 하는 모든 것을 도와드릴 준비가 되어 있습니다! 새 웹사이트를 만들거나 비즈니스가 더 원활하게 운영되도록 돕는 것까지, 언제든지 도와드리겠습니다!",
    "안녕하세요, 제품에 대한 추가 정보를 어디서 찾을 수 있나요?" : "저희 제품에 대한 모든 정보는 'Our Products' 페이지에서 확인하실 수 있습니다! 페이지를 살펴보시고, 궁금한 점이 있으면 언제든지 도와드리겠습니다! ",
    "안녕하세요, 가격에 대해 물어봐도 되나요?": "물론입니다! 가격에 대해 이야기하고 최고의 가치를 제공해 드리겠습니다. sales@yellowpenguin.co.kr로 이메일을 보내주시면, 간편하게 안내해 드리겠습니다!",
    "안녕하세요, Yellow Penguin에 대해 더 자세히 알려주실 수 있나요?" : "물론입니다! Yellow Penguin은 여러분의 기술적인 꿈을 실현시키는 회사입니다! 저희는 소프트웨어 개발부터 시스템 통합까지 다양한 서비스를 제공합니다. 펭귄 가족에 가입해 주세요!",
    "Yellow Penguin이란 무엇인가요?" : "Yellow Penguin은 고객의 요구에 맞춘 IT 시스템을 설계하고 구축하는 SI 플랫폼으로, 다양한 시스템을 원활하게 통합하여 운영됩니다",
    "귀사의 제품에 대한 자세한 정보를 어디에서 찾을 수 있나요?" : "저희 제품에 대한 자세한 정보는 홈페이지의 'Our Products' 섹션에서 확인하실 수 있습니다.",
    " 어떤 산업에 서비스를 제공하나요?": "저희는 다양한 산업에 맞춤형 시스템 통합 및 소프트웨어 솔루션을 제공하고 있습니다.",
    "웹사이트 구축 비용은 얼마인가요?": "웹사이트 구축 비용은 330,000원이며, 이는 일회성 결제입니다.",
    "홈페이지 구축/제작 비용/가격은 얼마인가요?": "사이트 구축 비용은 일회성 330,000원입니다.",

    #basic keywords
    "비용" : "가격에 대해 논의하고 가격 대비 솔루션 가치를 찾으려면 sales@yellowpenguin.co.kr로 이메일을 보내 주시면 쉽게 도와드리겠습니다! ",
    "가격" : "가격에 대해 논의하고 가격 대비 솔루션 가치를 찾으려면 sales@yellowpenguin.co.kr로 이메일을 보내 주시면 쉽게 도와드리겠습니다! ",
    "도움" : "저희는 언제든 도와드릴 준비가 되어 있습니다! 새 웹사이트 제작부터 비즈니스 운영 최적화까지, 필요한 모든 것을 지원해 드리겠습니다! 문의 사항이 있으시면 support@yellowpenguin.co.kr로 연락 주세요",
    "문의" : "문의사항이 있으시면 support@yellowpenguin.co.kr로 연락주세요",
    }

PREDEFINED_RESPONSES = get_predefined_responses()

def find_best_matches(user_input, PREDEFINED_RESPONSES, threshold=20): 
    """
    Finds one or more best matching questions based on a similarity threshold.
    """
    best_matches = []
    for question, answer in PREDEFINED_RESPONSES.items():
        similarity = fuzz.ratio(user_input.lower(), question.lower())
        print(similarity)
        if similarity >= threshold:
            best_matches.append((question, answer, similarity))
    
    # Sort by similarity (descending)
    best_matches.sort(key=lambda x: x[2], reverse=True) 
    return best_matches

def chatbot_response(user_input, PREDEFINED_RESPONSES):
    best_matches = find_best_matches(user_input, PREDEFINED_RESPONSES)
    print(best_matches)
    
    if not best_matches:
        # No matches above threshold - send to Gemini for a general response
        gemini_prompt = f"""
        You are a helpful, nice and formal chatbot. Answer the questions in the language user asked A user asked: "{user_input}"
        
        This question does not match any predefined responses. Please generate a friendly, concise, and helpful response.
        Keep it short and directly relevant to the question.
        """
        
        response = chat.send_message(gemini_prompt, stream=True)
        response_text = "".join(chunk.text for chunk in response)
        return response_text
    

    else:
        # One or more matches found - send to Gemini for refinement
        
        # Create a string of matched questions and answers
        matched_PREDEFINED_RESPONSES = "\n".join([f"Question: {q}\nAnswer: {a}" for q, a, _ in best_matches])

        gemini_prompt = f"""
        You are a helpful and friendly chatbot. Answer the questions in the language user asked: "{user_input}"

        Reply from the predefined responses:
        I found the following potentially relevant questions and answers in my knowledge base(Must answer from the predefined responses if the questions match.):

        {matched_PREDEFINED_RESPONSES}

        Based on these options, how would you best respond to the user's question? 
        Consider providing information from the matched Q&As or 
        offering a new response if none of them fully address the user's query. 
        Be concise, helpful, and address the user directly while keeping the answer short and sweet.
        """
        
        print(gemini_prompt)
        try:
            response = chat.send_message(gemini_prompt, stream=True)
            return "".join(chunk.text for chunk in response)
        except Exception:
            return "My apologies, but I'm not available at the moment. Please try again later after some times, thank you. Your patience is appreciated."


        # response = chat.send_message(gemini_prompt, stream=True)
        # response_text = "".join(chunk.text for chunk in response)

        # return response_text

@app.route("/api/generate", methods=["POST"])
def generate_api():
    try:
        data = request.get_json()
        user_input = data.get('question')
        if not user_input:
            return jsonify({'error': 'No question provided'}), 400

        response_text = chatbot_response(user_input, PREDEFINED_RESPONSES)
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


