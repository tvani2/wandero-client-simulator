import time
import re
from datetime import datetime

class ConversationAnalytics:
    def __init__(self):
        self.start_time = time.time()
        self.emails_sent = 0
        self.emails_received = 0
        self.response_times = []
        self.last_send_time = None
        self.last_message_id = None
        self.email_references = []
        
        # Analytics for testing Wandero's performance
        self.wandero_performance = {
            'response_times': [],  # How fast Wandero responds
            'response_quality': [],  # How well they answer questions
            'questions_answered': 0,  # How many client questions they answered
            'questions_ignored': 0,  # How many questions they missed
            'proposals_offered': 0,  # How many travel proposals they made
            'personalization_level': 0,  # How personalized their responses are
            'follow_up_questions': 0,  # How well they ask for missing info
            'upsell_attempts': 0,  # How many times they try to upsell
            'error_responses': 0,  # How many generic/error responses
            'specific_details_provided': 0,  # How specific their recommendations are
            'budget_consideration': 0,  # Whether they consider client budget
            'date_flexibility': 0,  # Whether they offer date alternatives
            'local_knowledge': 0,  # How much local knowledge they show
        }
        
        self.wandero_issues = {
            'missing_information': 0,  # Didn't ask for important details
            'slow_responses': 0,  # Responses taking too long
            'incomplete_answers': 0,  # Didn't answer all questions
            'poor_personalization': 0,  # Didn't personalize to client needs
            'lack_of_specifics': 0,  # Vague recommendations
            'no_follow_up': 0,  # Didn't follow up on important points
            'budget_ignored': 0,  # Ignored budget constraints
            'date_issues': 0,  # Problems with date handling
            'local_knowledge_gaps': 0  # Lack of local knowledge
        }
        
        self.wandero_strengths = {
            'quick_responses': 0,  # Fast response times
            'detailed_answers': 0,  # Comprehensive responses
            'good_questions': 0,  # Asked relevant follow-up questions
            'personalized_offers': 0,  # Personalized recommendations
            'budget_aware': 0,  # Considered budget constraints
            'flexible_dates': 0,  # Offered date alternatives
            'local_expertise': 0,  # Showed local knowledge
            'comprehensive_planning': 0,  # Complete travel planning
            'upsell_opportunities': 0  # Good upsell attempts
        }
    
    def record_email_sent(self, message_id=None):
        """Record when an email is sent"""
        self.emails_sent += 1
        self.last_send_time = time.time()
        if message_id:
            self.last_message_id = message_id
            self.email_references.append(message_id)
    
    def record_email_received(self):
        """Record when an email is received"""
        self.emails_received += 1
    
    def record_response_time(self):
        """Record response time if we have a last send time"""
        if self.last_send_time:
            response_time = time.time() - self.last_send_time
            self.response_times.append(response_time)
            return response_time
        return None
    
    def get_analytics_summary(self):
        """Get a summary of all analytics"""
        total_time = time.time() - self.start_time
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        
        summary = {
            'total_time_minutes': total_time / 60,
            'emails_sent': self.emails_sent,
            'emails_received': self.emails_received,
            'avg_response_time_minutes': avg_response_time / 60,
            'fastest_response_minutes': min(self.response_times) / 60 if self.response_times else 0,
            'slowest_response_minutes': max(self.response_times) / 60 if self.response_times else 0,
            'total_responses': len(self.response_times)
        }
        
        return summary
    
    def print_summary(self):
        """Print Wandero performance analysis"""
        summary = self.get_analytics_summary()
        performance_score = self.calculate_wandero_performance_score()
        
        print("\n" + "="*50)
        print("WANDERO PERFORMANCE ANALYSIS")
        print("="*50)
        
        # Basic metrics
        print(f"\nBASIC METRICS:")
        print(f"  • Total conversation time: {summary['total_time_minutes']:.1f} minutes")
        print(f"  • Emails sent by client: {summary['emails_sent']}")
        print(f"  • Emails received from Wandero: {summary['emails_received']}")
        print(f"  • Average response time: {summary['avg_response_time_minutes']:.1f} minutes")
        if self.response_times:
            print(f"  • Fastest response: {summary['fastest_response_minutes']:.1f} minutes")
            print(f"  • Slowest response: {summary['slowest_response_minutes']:.1f} minutes")
        
        # Performance score
        print(f"\nOVERALL PERFORMANCE SCORE: {performance_score:.1f}/100")
        
        # Wandero strengths
        print(f"\nWANDERO STRENGTHS:")
        strengths_found = False
        for strength, count in self.wandero_strengths.items():
            if count > 0:
                strength_name = strength.replace('_', ' ').title()
                print(f"  • {strength_name}: {count} times")
                strengths_found = True
        
        if not strengths_found:
            print("  • No significant strengths identified")
        
        # Wandero issues
        print(f"\nWANDERO ISSUES:")
        issues_found = False
        for issue, count in self.wandero_issues.items():
            if count > 0:
                issue_name = issue.replace('_', ' ').title()
                print(f"  • {issue_name}: {count} times")
                issues_found = True
        
        if not issues_found:
            print("  • No significant issues identified")
        
        # Performance breakdown
        print(f"\nPERFORMANCE BREAKDOWN:")
        print(f"  • Questions answered: {self.wandero_performance['questions_answered']}")
        print(f"  • Questions ignored: {self.wandero_performance['questions_ignored']}")
        print(f"  • Proposals offered: {self.wandero_performance['proposals_offered']}")
        print(f"  • Follow-up questions asked: {self.wandero_performance['follow_up_questions']}")
        print(f"  • Upsell attempts: {self.wandero_performance['upsell_attempts']}")
        
        # Recommendations
        print(f"\nRECOMMENDATIONS:")
        if self.wandero_issues['slow_responses'] > 0:
            print("  • Improve response time - clients expect faster replies")
        if self.wandero_issues['incomplete_answers'] > 0:
            print("  • Answer all client questions thoroughly")
        if self.wandero_issues['poor_personalization'] > 0:
            print("  • Personalize responses to client's specific needs")
        if self.wandero_issues['budget_ignored'] > 0:
            print("  • Always consider and mention budget constraints")
        if self.wandero_issues['local_knowledge_gaps'] > 0:
            print("  • Show more local expertise and cultural knowledge")
        
        if not any(self.wandero_issues.values()):
            print("  • Excellent performance! Keep up the great work!")
        
        print("\n" + "="*50)
    
    def analyze_wandero_response(self, wandero_message, client_questions=None):
        """Analyze Wandero's response for performance metrics"""
        text_lower = wandero_message.lower()
        
        # Track response time (already handled in record_response_time)
        
        # Analyze response quality (removed comprehensive/generic tracking)
        # Response length is subjective and not a reliable metric
        
        # Check if they answered client questions
        if client_questions:
            questions_asked = len(re.findall(r'\?', client_questions))
            questions_answered = 0
            for question in client_questions.split('?'):
                if question.strip() and any(word in text_lower for word in question.lower().split()):
                    questions_answered += 1
            
            if questions_answered >= questions_asked * 0.8:
                self.wandero_performance['questions_answered'] += questions_answered
                self.wandero_strengths['detailed_answers'] += 1
            else:
                self.wandero_performance['questions_ignored'] += (questions_asked - questions_answered)
                self.wandero_issues['incomplete_answers'] += 1
        
        # Check for proposals/offers
        if any(word in text_lower for word in ['proposal', 'offer', 'package', 'itinerary', 'plan']):
            self.wandero_performance['proposals_offered'] += 1
            self.wandero_strengths['comprehensive_planning'] += 1
        
        # Check for personalization
        if any(word in text_lower for word in ['your', 'based on', 'specifically', 'customized']):
            self.wandero_performance['personalization_level'] += 1
            self.wandero_strengths['personalized_offers'] += 1
        else:
            self.wandero_issues['poor_personalization'] += 1
        
        # Check for follow-up questions
        if any(word in text_lower for word in ['could you', 'would you', 'do you', 'what about', 'when']):
            self.wandero_performance['follow_up_questions'] += 1
            self.wandero_strengths['good_questions'] += 1
        
        # Check for upsell attempts
        if any(word in text_lower for word in ['premium', 'upgrade', 'additional', 'extra', 'luxury']):
            self.wandero_performance['upsell_attempts'] += 1
            self.wandero_strengths['upsell_opportunities'] += 1
        
        # Check for specific details
        if any(word in text_lower for word in ['$', 'dollar', 'euro', 'price', 'cost', 'budget']):
            self.wandero_performance['specific_details_provided'] += 1
            self.wandero_performance['budget_consideration'] += 1
            self.wandero_strengths['budget_aware'] += 1
        else:
            self.wandero_issues['budget_ignored'] += 1
        
        # Check for date flexibility
        if any(word in text_lower for word in ['alternative', 'different dates', 'flexible', 'change']):
            self.wandero_performance['date_flexibility'] += 1
            self.wandero_strengths['flexible_dates'] += 1
        else:
            self.wandero_issues['date_issues'] += 1
        
        # Check for local knowledge
        if any(word in text_lower for word in ['local', 'authentic', 'traditional', 'culture', 'custom']):
            self.wandero_performance['local_knowledge'] += 1
            self.wandero_strengths['local_expertise'] += 1
        else:
            self.wandero_issues['local_knowledge_gaps'] += 1
        
        # Check for professional tone (removed from tracking)
        # Professional tone is subjective and not a reliable metric
        
        # Check for generic responses (removed from tracking)
        # Generic response detection is subjective and not reliable
        
        # Check response speed
        if self.response_times and self.response_times[-1] < 300:  # Less than 5 minutes
            self.wandero_strengths['quick_responses'] += 1
        elif self.response_times and self.response_times[-1] > 1800:  # More than 30 minutes
            self.wandero_issues['slow_responses'] += 1
    
    def calculate_wandero_performance_score(self):
        """Calculate Wandero's overall performance score"""
        total_responses = self.emails_received
        
        if total_responses == 0:
            return 0.0
        
        # Calculate performance score based on various metrics
        score = 0.0
        max_score = 100.0
        
        # Response speed (25 points)
        if self.response_times:
            avg_response_time = sum(self.response_times) / len(self.response_times)
            if avg_response_time < 300:  # Less than 5 minutes
                score += 25
            elif avg_response_time < 900:  # Less than 15 minutes
                score += 20
            elif avg_response_time < 1800:  # Less than 30 minutes
                score += 15
            else:
                score += 5
        
        # Response quality (25 points)
        quality_score = 0
        if self.wandero_performance['questions_answered'] > self.wandero_performance['questions_ignored']:
            quality_score += 15
        if self.wandero_performance['proposals_offered'] > 0:
            quality_score += 10
        score += quality_score
        
        # Additional quality bonus (15 points)
        additional_score = 0
        if self.wandero_performance['follow_up_questions'] > 0:
            additional_score += 5
        if self.wandero_performance['date_flexibility'] > 0:
            additional_score += 5
        if self.wandero_performance['specific_details_provided'] > 0:
            additional_score += 5
        score += additional_score
        
        # Personalization (20 points)
        personalization_score = min(20, self.wandero_performance['personalization_level'] * 4)  # 5 levels × 4 points = 20 max
        score += personalization_score
        
        # Professional communication (removed from scoring)
        # Professional tone is subjective and not a reliable metric
        
        # Business acumen (15 points)
        business_score = 0
        if self.wandero_performance['budget_consideration'] > 0:
            business_score += 5
        if self.wandero_performance['upsell_attempts'] > 0:
            business_score += 5
        if self.wandero_performance['local_knowledge'] > 0:
            business_score += 5
        score += business_score
        
        return min(max_score, score)
    
    def get_threading_headers(self):
        """Get headers for email threading"""
        in_reply_to = self.last_message_id if self.last_message_id else None
        references = ' '.join(self.email_references) if self.email_references else None
        return in_reply_to, references 