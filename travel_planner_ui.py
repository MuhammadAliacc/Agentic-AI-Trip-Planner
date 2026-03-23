# travel_planner_ui.py
from nicegui import ui, app
import requests
import datetime
import asyncio
from typing import List
import os

BASE_URL = "http://localhost:8000"

# Travel themes and suggestions
TRAVEL_THEMES = [
    {"icon": "🏔️", "title": "Mountain Adventure", "description": "Himalayas, Alps, Rockies"},
    {"icon": "🏖️", "title": "Beach Paradise", "description": "Maldives, Bali, Caribbean"},
    {"icon": "🏙️", "title": "City Explorer", "description": "Tokyo, Paris, New York"},
    {"icon": "🌿", "title": "Nature Escape", "description": "Amazon, Safari, National Parks"},
    {"icon": "🍜", "title": "Culinary Journey", "description": "Italy, Japan, Thailand"},
    {"icon": "🎭", "title": "Cultural Immersion", "description": "India, Morocco, Peru"},
]

QUICK_SUGGESTIONS = [
    "✈️ Plan a 7-day romantic trip to Paris",
    "💰 Budget-friendly backpacking in Southeast Asia",
    "👨‍👩‍👧‍👦 Family vacation to Tokyo with kids",
    "💍 Luxury honeymoon in Maldives",
    "⛰️ Adventure trek in Patagonia",
    "🌸 Cultural tour of Japan during cherry blossom",
]

class ChatMessage:
    def __init__(self, content: str, is_user: bool, timestamp: datetime.datetime = None):
        self.content = content
        self.is_user = is_user
        self.timestamp = timestamp or datetime.datetime.now()

@ui.page('/')
def main_page():
    # Add custom CSS inside the page function
    ui.add_head_html('''
    <style>
        /* Modern CSS Reset & Variables */
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        
        /* Remove any default margins and make full width */
        body {
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }
        
        .nicegui-content {
            max-width: 100% !important;
            width: 100% !important;
            padding: 0 !important;
        }
        
        /* Smooth scrolling */
        html {
            scroll-behavior: smooth;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }
        
        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes bounce {
            0%, 80%, 100% {
                transform: scale(0);
            }
            40% {
                transform: scale(1);
            }
        }
        
        .fade-in-up {
            animation: fadeInUp 0.6s ease-out;
        }
        
        .slide-in {
            animation: slideIn 0.4s ease-out;
        }
        
        /* Glass morphism effect */
        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        
        /* Gradient text */
        .gradient-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Loading animation */
        .loading-dots {
            display: inline-flex;
            gap: 4px;
        }
        
        .loading-dots span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            animation: bounce 1.4s infinite ease-in-out both;
        }
        
        .loading-dots span:nth-child(1) { animation-delay: -0.32s; }
        .loading-dots span:nth-child(2) { animation-delay: -0.16s; }
        .loading-dots span:nth-child(3) { animation-delay: 0s; }
        
        /* Hover effects */
        .hover-lift {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .hover-lift:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        /* Message animations */
        .message-enter {
            animation: slideIn 0.4s ease-out;
        }
        
        /* Custom input styling */
        .custom-input .q-field__control {
            border-radius: 50px !important;
            background: white !important;
        }
        
        /* Gradient button */
        .gradient-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border-radius: 50px !important;
            padding: 0 24px !important;
            font-weight: 600 !important;
        }
        
        .gradient-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        /* Card hover effects */
        .theme-card {
            transition: all 0.3s ease;
        }
        
        .theme-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 25px -12px rgba(0, 0, 0, 0.2);
        }
        
        /* Custom header styling */
        .custom-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            width: 100%;
        }
        
        /* Custom footer input styling */
        .input-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            border-top: 1px solid rgba(0, 0, 0, 0.1);
            padding: 16px 24px;
            width: 100%;
        }
        
        /* Main content padding for fixed header and footer */
        .main-content {
            padding-top: 80px;
            padding-bottom: 100px;
            width: 100%;
            max-width: 100%;
        }
        
        /* Full width containers */
        .full-width {
            width: 100%;
            max-width: 100%;
        }
        
        /* Message containers full width */
        .message-row {
            width: 100%;
            padding: 0 20px;
        }
        
        /* Chat messages full width with appropriate padding */
        .message-card {
            max-width: 80%;
        }
        
        @media (max-width: 768px) {
            .message-card {
                max-width: 95%;
            }
            .message-row {
                padding: 0 12px;
            }
        }
        
        /* Hero section full width with gradient background */
        .hero-section {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border-radius: 0;
            margin: 0;
            padding: 40px 20px;
        }
        
        /* Content containers with proper spacing */
        .content-wrapper {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            width: 100%;
        }
        
        /* Full width sections */
        .full-section {
            width: 100%;
            padding: 20px 0;
        }
    </style>
    ''')
    
    # Set custom colors
    ui.colors(
        primary='#667eea',
        secondary='#764ba2',
        accent='#f093fb',
        positive='#10b981',
        negative='#ef4444',
        warning='#f59e0b'
    )
    
    # State variables
    messages = []
    is_processing = False
    loading_element = None  # Store reference to loading element
    
    # UI Elements
    input_field = None
    send_btn = None
    chat_container = None
    
    # Helper functions
    def scroll_to_top():
        ui.run_javascript('window.scrollTo({ top: 0, behavior: "smooth" })')
    
    def scroll_to_bottom():
        ui.run_javascript('window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" })')
    
    def add_welcome_message(container):
        welcome_msg = """### ✨ Welcome to your AI Travel Planner! ✨

I'm your intelligent travel assistant. I can help you with:

• **🎯 Custom itineraries** tailored to your preferences
• **💰 Budget optimization** and cost breakdowns  
• **🌟 Hidden gems** and local experiences
• **🌤️ Weather insights** and best times to visit
• **📚 Cultural tips** and language essentials

**Just tell me where you want to go, your travel style, and any special requirements!** 🚀

---
*Example: "Plan a 5-day budget trip to Thailand with focus on beaches and street food"*
"""
        
        with container:
            with ui.row().classes('justify-center w-full'):
                with ui.card().classes('glass-card p-6 message-card slide-in mb-4').style('border-left: 4px solid #667eea'):
                    with ui.row().classes('items-start gap-3'):
                        ui.label('🤖').classes('text-3xl')
                        with ui.column().classes('flex-grow'):
                            ui.markdown(welcome_msg).classes('text-gray-700')
                            with ui.row().classes('gap-2 mt-2'):
                                ui.label(f"🕐 {datetime.datetime.now().strftime('%I:%M %p')}").classes('text-xs text-gray-400')
                                ui.label(f"📅 {datetime.datetime.now().strftime('%B %d, %Y')}").classes('text-xs text-gray-400')
    
    def add_message_card(container, message):
        with container:
            alignment = 'justify-end' if message.is_user else 'justify-start'
            
            with ui.row().classes(f'w-full {alignment} message-enter mb-4'):
                if not message.is_user:
                    with ui.element('div').classes('mr-2'):
                        ui.label('🤖').classes('text-2xl')
                
                with ui.card().classes(f'message-card p-4 {"bg-gradient-to-r from-purple-500 to-pink-500 text-white" if message.is_user else "glass-card"}').style('border-radius: 20px;'):
                    if message.is_user:
                        ui.label('You').classes('text-xs opacity-80 mb-1')
                        ui.label(message.content).classes('text-white font-medium')
                    else:
                        ui.markdown(message.content).classes('text-gray-800')
                    
                    with ui.row().classes('justify-end mt-2 gap-2'):
                        ui.label(message.timestamp.strftime('%I:%M %p')).classes('text-xs opacity-70')
                
                if message.is_user:
                    with ui.element('div').classes('ml-2'):
                        ui.label('👤').classes('text-2xl')
    
    def add_loading_indicator(container):
        """Add loading indicator and return its container for later removal"""
        with container:
            with ui.row().classes('justify-start items-start mb-4') as loading_row:
                ui.label('🤖').classes('text-2xl mr-2')
                with ui.card().classes('glass-card p-4 message-card').style('border-radius: 20px;'):
                    with ui.element('div').classes('loading-dots mb-2'):
                        ui.element('span')
                        ui.element('span')
                        ui.element('span')
                    ui.label('AI is crafting your perfect itinerary...').classes('text-sm text-gray-500')
            return loading_row
    
    def format_travel_plan(answer):
        current_time = datetime.datetime.now()
        
        formatted = f"""## 🌟 Your Personalized Travel Plan

**Generated:** {current_time.strftime('%B %d, %Y at %H:%M')}  
**Created by:** Atriyo's AI Travel Agent

---

{answer}

---

### ✨ Pro Tips for Your Journey:

| Category | Tips |
|----------|------|
| 📸 **Attractions** | Book popular spots in advance to avoid queues |
| 💰 **Budget** | Check currency rates and inform your bank about travel |
| 🌡️ **Weather** | Verify seasonal conditions before packing |
| 📱 **Tech** | Download offline maps and translation apps |
| 🏥 **Safety** | Get travel insurance for peace of mind |

---
*This AI-generated plan is designed to inspire your journey. Please verify all details with official sources before booking.*

**Safe travels! 🌍✨**"""
        
        return formatted
    
    async def send_message():
        nonlocal is_processing, loading_element
        user_input = input_field.value
        if not user_input or not user_input.strip() or is_processing:
            return
        
        is_processing = True
        send_btn.disable()
        
        # Add user message
        user_msg = ChatMessage(user_input, True)
        messages.append(user_msg)
        add_message_card(chat_container, user_msg)
        input_field.value = ''
        
        # Scroll to show the new message
        scroll_to_bottom()
        
        # Add loading indicator and store reference
        loading_element = add_loading_indicator(chat_container)
        
        # Scroll to show loading indicator
        scroll_to_bottom()
        
        try:
            payload = {"question": user_input}
            
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: requests.post(f"{BASE_URL}/query", json=payload, timeout=30)
            )
            response.raise_for_status()
            data = response.json()
            answer = data.get("answer", "No answer returned.")
            
            formatted_answer = format_travel_plan(answer)
            
            # Remove loading indicator
            if loading_element:
                loading_element.clear()
                loading_element = None
            
            # Add AI response
            ai_msg = ChatMessage(formatted_answer, False)
            messages.append(ai_msg)
            add_message_card(chat_container, ai_msg)
            
            # Auto-scroll to bottom
            scroll_to_bottom()
            
        except requests.exceptions.Timeout:
            if loading_element:
                loading_element.clear()
                loading_element = None
            with chat_container:
                with ui.row().classes('justify-start w-full mb-4'):
                    with ui.card().classes('bg-red-50 border-l-4 border-red-500 p-4 message-card').style('border-radius: 12px;'):
                        ui.label('⏰ Request timeout. Please try again.').classes('text-red-700 font-medium')
            scroll_to_bottom()
        except requests.exceptions.ConnectionError:
            if loading_element:
                loading_element.clear()
                loading_element = None
            with chat_container:
                with ui.row().classes('justify-start w-full mb-4'):
                    with ui.card().classes('bg-red-50 border-l-4 border-red-500 p-4 message-card').style('border-radius: 12px;'):
                        ui.label('🔌 Cannot connect to backend. Please ensure the server is running on port 8000.').classes('text-red-700 font-medium')
            scroll_to_bottom()
        except Exception as e:
            if loading_element:
                loading_element.clear()
                loading_element = None
            with chat_container:
                with ui.row().classes('justify-start w-full mb-4'):
                    with ui.card().classes('bg-red-50 border-l-4 border-red-500 p-4 message-card').style('border-radius: 12px;'):
                        ui.label(f'❌ Error: {str(e)}').classes('text-red-700 font-medium')
            scroll_to_bottom()
        finally:
            is_processing = False
            send_btn.enable()
    
    def clear_chat():
        nonlocal messages, loading_element
        if loading_element:
            loading_element.clear()
            loading_element = None
        chat_container.clear()
        messages = []
        add_welcome_message(chat_container)
        ui.notify('✨ Chat cleared! Ready for new adventures', type='positive', position='top')
        scroll_to_top()
    
    def export_chat():
        ui.notify('📄 Export feature coming soon!', type='info', position='top')
    
    def set_input(text):
        input_field.value = text
        ui.run_javascript('document.querySelector("input")?.focus()')
    
    # Header - Fixed at top full width
    with ui.header().classes('custom-header').style('background: transparent; box-shadow: none; width: 100%;'):
        with ui.element('div').classes('glass-card w-full').style('border-radius: 0;'):
            with ui.row().classes('content-wrapper w-full px-4 py-3 items-center justify-between'):
                with ui.row().classes('items-center gap-3 cursor-pointer').on('click', scroll_to_top):
                    with ui.element('div').classes('text-4xl animate-pulse'):
                        ui.label('🌍')
                    with ui.column().classes('gap-0'):
                        ui.label('Travel Planner Agent').classes('text-2xl font-bold gradient-text')
                        ui.label('AI-Powered Travel Intelligence').classes('text-xs text-gray-500')
                
                with ui.row().classes('gap-2'):
                    ui.button('✨ New Chat', on_click=clear_chat).props('flat').classes('text-purple-600')
                    ui.button('📋 Export', on_click=export_chat).props('flat').classes('text-purple-600')
    
    # Main scrollable content area - Full width
    with ui.element('div').classes('main-content min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 full-width'):
        # Animated background elements
        with ui.element('div').classes('fixed inset-0 overflow-hidden pointer-events-none'):
            with ui.element('div').classes('absolute -top-40 -right-40 w-80 h-80 rounded-full bg-gradient-to-r from-purple-200 to-pink-200 opacity-30 blur-3xl'):
                pass
            with ui.element('div').classes('absolute -bottom-40 -left-40 w-80 h-80 rounded-full bg-gradient-to-r from-blue-200 to-indigo-200 opacity-30 blur-3xl'):
                pass
        
        # Hero Section - Full width
        with ui.element('div').classes('hero-section full-section'):
            with ui.element('div').classes('content-wrapper'):
                with ui.card().classes('glass-card p-8 text-center hover-lift'):
                    ui.label('Where would you like to explore today?').classes('text-4xl font-bold mb-3 gradient-text')
                    ui.label('Let our AI create your perfect journey').classes('text-gray-600 text-lg mb-6')
                    ui.label('💡 Type your question in the input box below!').classes('text-sm text-purple-600 font-semibold')
        
        # Quick Suggestions Section - Full width
        with ui.element('div').classes('full-section'):
            with ui.element('div').classes('content-wrapper'):
                with ui.column().classes('mb-8 fade-in-up'):
                    ui.label('✨ Quick Inspiration').classes('text-xl font-bold mb-3')
                    with ui.row().classes('gap-3 flex-wrap justify-center'):
                        for suggestion in QUICK_SUGGESTIONS[:4]:
                            with ui.card().classes('p-3 cursor-pointer hover-lift bg-white/80').on('click', lambda s=suggestion: set_input(s)):
                                ui.label(suggestion).classes('text-sm text-gray-700')
        
        # Travel Themes Section - Full width
        with ui.element('div').classes('full-section'):
            with ui.element('div').classes('content-wrapper'):
                with ui.column().classes('mb-8 fade-in-up'):
                    ui.label('🎯 Travel Themes').classes('text-xl font-bold mb-3')
                    with ui.grid(columns=3).classes('gap-4'):
                        for theme in TRAVEL_THEMES:
                            with ui.card().classes('p-4 text-center cursor-pointer theme-card bg-white/80').on('click', lambda t=theme['title']: set_input(f"Plan a {t} trip")):
                                ui.label(theme['icon']).classes('text-4xl mb-2')
                                ui.label(theme['title']).classes('font-semibold text-gray-800')
                                ui.label(theme['description']).classes('text-xs text-gray-500 mt-1')
        
        # Chat History Container - Full width
        with ui.element('div').classes('full-section'):
            with ui.element('div').classes('content-wrapper'):
                chat_container = ui.column().classes('w-full space-y-2')
                
                # Welcome message
                add_welcome_message(chat_container)
    
    # Fixed Input Footer at Bottom - Full width
    with ui.footer().classes('input-footer').style('width: 100%;'):
        with ui.row().classes('content-wrapper w-full gap-3 items-center'):
            with ui.element('div').classes('flex-grow'):
                input_field = ui.input(
                    placeholder='✍️ Type your message here... (Press Enter to send)',
                ).props('outlined dense').classes('w-full text-base')
                input_field.classes('bg-white rounded-full custom-input')
                input_field.on('keydown.enter', send_message)
            
            send_btn = ui.button('Send Message ✨', on_click=send_message)
            send_btn.classes('gradient-btn')
            
            # Quick scroll buttons
            ui.button('⬆️ Top', on_click=scroll_to_top).props('flat').classes('text-purple-600')
            ui.button('⬇️ Bottom', on_click=scroll_to_bottom).props('flat').classes('text-purple-600')

if __name__ == '__main__':
    ui.run(
        title='🌍 AI Travel Planner - Your Personal Travel Assistant',
        favicon='🌍',
        port=8080,
        reload=False,
        show=True,
        host='0.0.0.0'
    )