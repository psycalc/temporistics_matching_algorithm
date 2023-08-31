from relationship_calculator import Typology

class TypologyPsychosophia(Typology):
    def __init__(self):
        """
        Initializes a new instance of the TypologyPsychosophia class.
        """
        super().__init__(["Emotion", "Logic", "Will", "Power"])
    
    def get_all_quadras(self):
        """
        Returns all quadras of psychosophy with their descriptions.
        
        Each quadra consists of four types that share common values and characteristics.
        """
        quadras = {
            'First': {
                'types': ['Andersen (ELWF)', 'Ghazali (EWLV)', 'Goethe (PWLE)', 'Aristippus (PLWE)'],
                'description': 'The first psychosophic quadra is characterized by processional Will and Logic, as well as resultative Physics and Emotion. Its representatives value arguments and heated discussions. Proving one\'s rightness is important for the types of this quadra, because their self-esteem depends significantly on it. These types are usually unpretentious in everyday life and entertainment, which is why their personal relationships are the strongest compared to other quadras. At the same time, they are ambitious, like to discuss their goals and decisions.'
            },
            'Second': {
                'types': ['Pushkin (EPWL)', 'Pasternak (EWPL)', 'Lao Tzu (LPWE)', 'Plato (LWPE)'],
                'description': 'The second psychosophic quadra is characterized by processional Will and Physics, as well as resultative Emotion and Logic. It includes such types as Pushkin (EPWL), Pasternak (EWPL), Lao Tzu (LPWE) and Plato (LWPE). This quadra can be called "the most silent" of all, since those aspects that are primarily manifested through speech (Emotion with Logic) are in positions of functions with the property "result". For these types, the collective and interaction with it are very important. They like to cooperate and compete with other people, gather a team to achieve goals and develop joint strategies. Also for them, the primary issue is the beauty and aesthetics of the material world. They have a desire to decorate and bring to perfection their place of residence or work. In people, they value grooming more than just a beautiful appearance. For them it is important that a person constantly improves, making efforts for this, and only such people, in their understanding, deserve respect. The strong sides of the types of the second quadra are: the ability to achieve long-term goals, good taste, care for their health, tolerance for stormy emotional manifestations, constant work on themselves. Their weak sides are unwillingness to question established dogmas, lack of charisma and low level of empathy.'
            },
            'Third': {
                'types': ['Rousseau (ELFW)', 'Bukharin (EWFL)', 'Napoleon (PFLW)', 'Lenin (PLWF)'],
                'description': 'The third psychosophic quadra is characterized by processional Physics and Logic, as well as resultative Will and Emotion. It includes such types as Rousseau (ELFW), Bukharin (EWFL), Napoleon (PFLW) and Lenin (PLWF). Its representatives are "people of the Renaissance era" who make the world beautiful and spiritualized. These types are active and mobile, constantly improving their body, love walks and nature. This helps them get a lot of pleasure from life, maintain good health for many years. And an inexhaustible interest in knowing the world makes them study a lot, think, discuss on all sorts of philosophical topics. Types of the third quadra show themselves well in intellectual activity, as well as in those types of art that require excellent mastery of technique - handicrafts, drawing, classical dances and music. Their strong sides are freethinking, naturalness, subtle understanding of aesthetics. Their weak sides are uncompromisingness and fussiness, a tendency to believe in beautifully designed but unconfirmed concepts.' 
            }
            
        }
        
        
        return quadras

