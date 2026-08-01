class ActiveInferenceInstitute:
    def __init__(self):
        self.organization_info = self._define_organization_info()
        self.worldview = self._define_worldview()
        self.implications = self._define_implications()
        self.stances = self._define_stances()
        self.beliefs = self._define_beliefs()
        self.quotes = self._define_quotes()
        self.activities = self._define_activities()
        self.board_of_directors = self._define_board_of_directors()
        self.scientific_advisory_board = self._define_scientific_advisory_board()
        self.research_fellows = self._define_research_fellows()

    def _define_organization_info(self):
        return {
            "type": "501(c)(3) educational non-profit",
            "location": "Delaware, USA",
            "status": "All-volunteer organization"
        }

    def _define_worldview(self):
        return {
            "ontology": "Active Inference models cognition and behavior as the active minimization of prediction error.",
            "epistemology": "Active Inference provides a unified approach for modeling, designing, and implementing systems across scales and disciplines.",
            "transdisciplinarity": True,
            "core_concepts": [
                "Variational Free Energy", "Prediction Error Minimization", "Self-Organization",
                "Complex Adaptive Systems", "Bayesian Inference", "Embodied Cognition",
                "Markov Blankets", "Generative Models", "Expected Free Energy",
                "Epistemic Foraging", "Participatory Sense-Making", "Circular Causality",
                "Autopoiesis", "Allostasis", "Information Geometry"
            ],
            "methodologies": [
                "Theoretical and applied Active Inference", "Free Energy Principle",
                "Bayesian Modeling", "Global online learning", "Online, Hybrid, and In-person events",
                "Organizational partnerships", "Dynamical Systems Theory", "Information Theory",
                "Neuroscientific Methods", "Computational Psychiatry", "Neurophenomenology",
                "Variational Methods", "RxInfer.jl for Multiscale Modeling", "Action Research",
                "Volunteer Programs", "Internships", "Mentorship Programs", "Open Science",
                "Open Source", "Textbook and Learning Groups", "Technical and Scientific skill development",
                "Participatory Global Research", "Knowledge Engineering", "Symbolic Cognitive Robotics"
            ],
            "perspectives": [
                "Holistic", "Interdisciplinary", "Systems Thinking", "Open Science",
                "Participatory Global Research", "Inclusive Communication",
                "Neurodiversity-Affirming", "Sustainability-Oriented", "Ethical AI Development"
            ]
        }

    def _define_implications(self):
        return {
            "cognitive_science": "Bridges descriptive cognition and prescriptive AI approaches.",
            "artificial_intelligence": "Guides ethical AI development and information system integration.",
            "social_sciences": "Models social systems and collective behavior.",
            "health": "Applications in clinical psychiatry and human health.",
            "education": "Supports educational materials and neurodivergent learning.",
            "ecology": "Insights into ecological dynamics and sustainability.",
            "economics": "Informs economic modeling and decision-making.",
            "robotics": "Applied in symbolic cognitive robotics.",
            "linguistics": "Models human translation processes.",
            "philosophy": "Contributes to discussions on self, consciousness, and communication.",
            "game_design": "Implemented in game design with aligned incentives.",
            "arts_and_mathematics": "Illuminates connections between mathematics and the arts."
        }

    def _define_stances(self):
        return {
            "open_source": True, "interdisciplinary_collaboration": True,
            "community_engagement": True, "sustainability": True,
            "scalability": True, "automation": True,
            "ethical_ai": True, "data_privacy": True,
            "transparency": True, "accessibility": True,
            "applicability": True, "rigor": True,
            "participatory_research": True, "global_open_science": True,
            "neurodiversity_affirmation": True, "inclusive_communication": True,
            "creative_exploration": True
        }

    def _define_beliefs(self):
        return {
            "core_values": [
                "Inclusivity", "Accessibility", "Productivity", "Integrity", "Safety",
                "Ethical Responsibility", "Transparency", "Excellence", "Collaboration",
                "Innovation", "Sustainability", "Neurodiversity", "Interdisciplinarity"
            ],
            "principles": [
                "Minimization of Prediction Error", "Self-Organization",
                "Transdisciplinary Integration", "Open Source Collaboration",
                "Ethical AI Development", "Data Privacy", "Active Inference and Exploration",
                "Dynamic Internal Modeling", "Anticipatory Behavior", "Continuous Development",
                "Participatory Sense-Making", "Inclusive Knowledge Sharing",
                "Creative Problem-Solving"
            ],
            "goals": [
                "Sustainable implementation of administrative and governance functions.",
                "Develop publishing and licensing protocols.",
                "Ensure stability and minimize risk within the ecosystem.",
                "Operate cyber and cognitive security systems.",
                "Promote ethical AI practices and data privacy.",
                "Foster interdisciplinary research and collaboration.",
                "Advance education and scientific literacy.",
                "Improve community user experience and design systems.",
                "Develop communications and public relations strategies.",
                "Support workforce development and competency evaluation.",
                "Cultivate an inclusive and accessible learning environment.",
                "Bridge theoretical concepts with practical applications.",
                "Facilitate global participation in active inference research and development."
            ],
            "ecosystem_structure": {
                "description": "Cultivates an active and engaged ecosystem around Active Inference, emphasizing accessibility, applicability, and rigor in a participatory global open science setting.",
                "components": [
                    "Participants (Members and Learners)", "Users (Adopters and Beneficiaries)",
                    "Research Partners (External Research Organizations and Working Groups)",
                    "Educational Partners (Universities and Educators)", "Funders (Donors, Supporters, and Funding Agencies)",
                    "Community Contributors (Open Source Developers, Content Creators)",
                    "Interdisciplinary Collaborators (Artists, Philosophers, Game Designers)"
                ]
            },
            "tech_stack": [
                "Coda (Modeling, Project, and Knowledge Management Platform)",
                "YouTube (Live Streaming and Video Hosting)", "Discord (Forum and Instant Messaging)",
                "Google Workspace (Document Management, Document Production, and Email)",
                "Twitter (now 'X') (Public Announcements and Releases)", "RxInfer.jl (Multiscale Modeling Tool)",
                "Open Source Development Platforms (for collaborative coding and knowledge sharing)"
            ],
            "organizational_structure": {
                "board_of_directors": "Operational since the end of 2022",
                "scientific_advisory_board": "Comprises external experts in Active Inference and related research areas",
                "officers": {
                    "president_and_treasurer": "Daniel Friedman",
                    "vice_president": "Alexander Vyatkin",
                    "secretary": "Bleu Knight"
                },
                "organizational_units": [
                    "Education Unit (EduActive)", "Administrative Unit (Institute-scale)",
                    "Research and Development Unit (ReInference)"
                ]
            }
        }

    def _define_quotes(self):
        return [
            "The Institute contributes to participants' self-efficacy, safety, and impact.",
            "The Active Inference Institute attracts and amplifies the self-organizing abilities of people.",
            "The Institute's work and community building efforts exemplify the benefits of 'open' systems.",
            "Active Inference is an integrated physics-based approach to modeling cognition and behavior.",
            "Active Inference bridges descriptive approaches to cognition and prescriptive approaches to AI and design.",
            "Active Inference enables a principled account of composition and decomposition in complex adaptive systems.",
            "The transdisciplinary nature and flexibility of Active Inference makes it ideal for work across myriad use-cases.",
            "Rapid growth comes with new challenges and greater requirements for sustainability.",
            "The Institute will establish user-experience auditing and common design patterns.",
            "The Institute seeks financial and operational support to scale our impact and pursue sustainability.",
            "We believe in the power of participatory global research to advance our understanding of active inference.",
            "Our approach to education is inclusive, recognizing and valuing neurodiversity in learning styles.",
            "The Active Inference Institute is committed to bridging the gap between theoretical concepts and real-world applications."
        ]

    def _define_activities(self):
        return {
            "eduactive_projects": {
                "institute": [
                    "Active Inference Ontology", "Audio-Visual Production",
                    "Textbook Group (Parr, Pezzulo, Friston 2022)", "Active Inference Journal"
                ],
                "ecosystem": [
                    "Action Research on Collective Foraging", "Solving the Tower of Babel Problem: UniFysica Philo-sophia",
                    "Numinia", "MathArt Conversations", "Neurodivergent Learning Sessions",
                    "Draft Book: The Physics of a Fulfilling Life"
                ]
            },
            "reinference_projects": {
                "institute": [
                    "RxInfer.jl Learning and Development Group", "Knowledge Engineering",
                    "Active Blockference"
                ],
                "ecosystem": [
                    "Symbolic Cognitive Robotics", "Active Inference Account of Belief Updating in PTSD",
                    "Humanity's Story of an Uncertain Self", "An Active Inference Agent for Modeling Human Translation Processes",
                    "Improving RxInfer.jl's Model Visualization Capabilities"
                ]
            }
        }

    def _define_board_of_directors(self):
        return [
            {"name": "John Clippinger", "statement": "I want to bring Active Inference into a broad range of applications, specifically into a new model of the firm, markets and finance."},
            {"name": "Daniel Friedman", "statement": "I expect and prefer to integrate the Institute's daily operations with our broader vision."},
            {"name": "Rafael Kaufmann", "statement": "I build adaptive sociotechnical systems that help human collectives, from teams to civilizations."},
            {"name": "Bleu Knight", "statement": "I ensure that our actions align with our values and strategic objectives, thus generating the sensations we prefer."},
            {"name": "Mike Smith", "statement": "I contribute to strategies for service and education, and facilitate epistemic foraging with active inference in commercial applications."},
            {"name": "Dean Tickles", "statement": "I see my role as a supplier of blind spot remover and a suggester of 'Escape Room' strategies as we open up active inferring."}
        ]

    def _define_scientific_advisory_board(self):
        return [
            "Mahault Albarracin", "Bradly Alicea", "Sebastian Alvarado", "John Boik",
            "Matt Brown", "John Cook", "Scott David", "Renée Davis", "Shanna Dobson",
            "Shady El Damaty", "Jeff Emmett", "Chris Fields", "Karl Friston",
            "Holly Grimm", "Avel GUÉNIN—CARLUT", "Sarah Hamburg", "Susan Hasty",
            "Conor Heins", "Susan Keen", "Thomas Kehler", "Héctor Manrique",
            "Alexandra Mikhailova", "Haris Neophytou", "Alexander Ororbia",
            "Sandeep Ramesh", "Maxwell J. D. Ramstead", "Adeel Razi",
            "Manuel Razo-Mejia", "Jakub Smekal", "Ian Tennant", "Mick Thacker",
            "Shingai Thornton", "Mark Wilcox", "Michael Zargham"
        ]

    def _define_research_fellows(self):
        return [
            {
                "name": "Anna Pereira",
                "period": "May 2024 - ",
                "project": "Cultivating a grass roots impact project to explore rapid dissemination of Active Inference Principles. The project actively provides mutualistic opportunities for collaboration and seeks to build community."
            },
            {
                "name": "Jean-Francois Cloutier",
                "period": "May 2024 - ",
                "project": "I seek to find out what it takes, at a minimum, for a robot to learn, on its own, how to survive in a world it knows initially almost nothing about. My research is the continuation of a project of many years in which I program simple autonomous robots to develop and ground my understanding of cognition."
            },
            {
                "name": "John Boik",
                "period": "May 2024 - ",
                "project": "As an Active Inference Institute Research Fellow, the research program I will pursue is a continuation of the work I describe in a book and in two series of concept papers. That program explores the science-driven, de novo development of new cognitive architectures that are, by design, fit for purpose. The first series describes how the approach can be applied to the creation of new societal systems (e.g., new economic and governance systems), which are viewed as components of a society's cognitive architecture. The second series describes how the approach can be applied to creation of an online ecosystem that facilitates cognition in the large-group setting.",
            }
        ]

        # (orphaned fragment - preserved verbatim)
        # "Online, Hybrid, and In-person events",
        #     "Organizational partnerships", "Dynamical Systems Theory", "Information Theory",
        #     "Neuroscientific Methods", "Computational Psychiatry", "Neurophenomenology",
        #     "Variational Methods", "RxInfer.jl for Multiscale Modeling", "Action Research",
        #     "Volunteer Programs", "Internships", "Mentorship Programs", "Open Science",
        #     "Open Source", "Textbook and Learning Groups", "Technical and Scientific skill development",
        #     "Participatory Global Research", "Knowledge Engineering", "Symbolic Cognitive Robotics"
        # ],
        # "perspectives": [
        #     "Holistic", "Interdisciplinary", "Systems Thinking", "Open Science",
        #     "Participatory Global Research", "Inclusive Communication",
        #     "Neurodiversity-Affirming", "Sustainability-Oriented", "Ethical AI Development"
        # ]
        # }

    def _define_implications(self):
        return {
            "cognitive_science": "Active Inference bridges descriptive approaches to cognition and prescriptive approaches to AI and design.",
            "artificial_intelligence": "Active Inference guides the integration and management of heterogeneous information systems, promoting ethical AI development.",
            "social_sciences": "Active Inference enables modeling of social systems and collective behavior, including team formation praxis.",
            "health": "Active Inference has applications in clinical psychiatry and human health, including modeling belief updating in PTSD and exploring wellness through an active inference lens.",
            "education": "Active Inference supports the development of educational materials and competency standards, including neurodivergent learning approaches and innovative textbook study methods.",
            "ecology": "Active Inference provides insights into ecological dynamics and sustainability, informing collective foraging practices.",
            "economics": "Active Inference informs economic modeling and decision-making processes, potentially influencing sustainable practices.",
            "robotics": "Active Inference is applied in symbolic cognitive robotics, exploring societies of mind and mortal computing.",
            "linguistics": "Active Inference is used to model human translation processes and address communication challenges across disciplines.",
            "philosophy": "Active Inference contributes to discussions on the nature of self, consciousness, and human narratives, including the development of inclusive systems of communication.",
            "game_design": "Active Inference principles are implemented in game design with aligned incentives, as demonstrated in projects like Numinia.",
            "arts_and_mathematics": "Active Inference helps illuminate connections between mathematics and the arts, fostering creative interdisciplinary exploration."
        }

    def _define_stances(self):
        return {
            "open_source": True, "interdisciplinary_collaboration": True,
            "community_engagement": True, "sustainability": True,
            "scalability": True, "automation": True,
            "ethical_ai": True, "data_privacy": True,
            "transparency": True, "accessibility": True,
            "applicability": True, "rigor": True,
            "participatory_research": True, "global_open_science": True,
            "neurodiversity_affirmation": True, "inclusive_communication": True,
            "creative_exploration": True
        }

    def _define_beliefs(self):
        return {
            "core_values": [
                "Inclusivity", "Accessibility", "Productivity", "Integrity", "Safety",
                "Ethical Responsibility", "Transparency", "Excellence", "Collaboration",
                "Innovation", "Sustainability", "Neurodiversity", "Interdisciplinarity"
            ],
            "principles": [
                "Minimization of Prediction Error", "Self-Organization",
                "Transdisciplinary Integration", "Open Source Collaboration",
                "Ethical AI Development", "Data Privacy", "Active Inference and Exploration",
                "Dynamic Internal Modeling", "Anticipatory Behavior", "Continuous Development",
                "Participatory Sense-Making", "Inclusive Knowledge Sharing",
                "Creative Problem-Solving"
            ],
            "goals": [
                "Establish sustainable implementation of administrative and governance functions.",
                "Develop publishing and licensing protocols.",
                "Provide services to ensure stability and minimize risk within the ecosystem.",
                "Organize and operate cyber and cognitive security systems.",
                "Promote ethical AI practices and data privacy.",
                "Foster interdisciplinary research and collaboration.",
                "Advance education and scientific literacy.",
                "Improve community user experience and design systems.",
                "Develop communications and public relations strategies.",
                "Support workforce development and competency evaluation.",
                "Cultivate an inclusive and accessible learning environment.",
                "Bridge theoretical concepts with practical applications across disciplines.",
                "Facilitate global participation in active inference research and development."
            ],
            "ecosystem_structure": {
                "description": "The Institute cultivates an active and engaged ecosystem around the scientific modeling framework of Active Inference, emphasizing accessibility, applicability, and rigor in a participatory global open science setting.",
                "components": [
                    "Participants (Members and Learners)",
                    "Users (Adopters and Beneficiaries)",
                    "Research Partners (External Research Organizations and Working Groups)",
                    "Educational Partners (Universities and Educators)",
                    "Funders (Donors, Supporters, and Funding Agencies)",
                    "Community Contributors (Open Source Developers, Content Creators)",
                    "Interdisciplinary Collaborators (Artists, Philosophers, Game Designers)"
                ]
            },
            "tech_stack": [
                "Coda (Modeling, Project, and Knowledge Management Platform)",
                "YouTube (Live Streaming and Video Hosting)",
                "Discord (Forum and Instant Messaging)",
                "Google Workspace (Document Management, Document Production, and Email)",
                "Twitter (now 'X') (Public Announcements and Releases)",
                "RxInfer.jl (Multiscale Modeling Tool)",
                "Open Source Development Platforms (for collaborative coding and knowledge sharing)"
            ],
            "organizational_structure": {
                "board_of_directors": "Operational since the end of 2022",
                "scientific_advisory_board": "Comprises external experts in Active Inference and related research areas",
                "officers": {
                    "president_and_treasurer": "Daniel Friedman",
                    "vice_president": "Alexander Vyatkin",
                    "secretary": "Bleu Knight"
                },
                "organizational_units": [
                    "Education Unit (EduActive)",
                    "Administrative Unit (Institute-scale)",
                    "Research and Development Unit (ReInference)",
                ]
            }
        }

    def _define_quotes(self):
        return [
            "The Institute contributes to participants' (i) self-efficacy, (ii) safety, and (iii) impact, through the aims of our broader vision and strategy.",
            "The Active Inference Institute attracts and amplifies the self-organizing abilities of people, thereby potentiating a unique opportunity and a powerful and scalable platform from which to accomplish research and development goals.",
            "The Institute's work and community building efforts have always exemplified the benefits of 'open' systems, consistent with the insights gleaned from Active Inference research itself.",
            "Active Inference is an integrated physics-based approach to modeling cognition and behavior as the active minimization of prediction error.",
            "The generality and action orientation of Active Inference makes it a natural bridge between descriptive approaches to cognition (e.g., biology) and prescriptive approaches to implementation of artificial intelligence (e.g., machine learning) and design (e.g., user experience, communication).",
            "Active Inference therefore enables a principled account of composition and decomposition, construction and de-construction, in complex adaptive systems.",
            "The transdisciplinary nature and flexibility of Active Inference makes the framework ideal for practical, theoretical, and interoperable work across myriad use-cases.",
            "Rapid growth comes with new challenges and greater requirements for sustainability.",
            "The Institute will establish user-experience auditing and common design patterns to ensure a satisfactory, calm, and reliable user experience, as well as the smooth delivery of bug reports and feedback.",
            "The Institute seeks financial and operational support to scale our impact in the coming years and pursue sustainability.",
            "We believe in the power of participatory global research to advance our understanding of active inference and its applications across diverse fields.",
            "Our approach to education is inclusive, recognizing and valuing neurodiversity in learning styles and cognitive approaches.",
            "The Active Inference Institute is committed to bridging the gap between theoretical concepts and real-world applications, fostering innovation across disciplines."
        ]

    def _define_activities(self):
        return {
            "eduactive_projects": {
                "institute": [
                    "Active Inference Ontology",
                    "Audio-Visual Production",
                    "Textbook Group (Parr, Pezzulo, Friston 2022)",
                    "Active Inference Journal"
                ],
                "ecosystem": [
                    "Action Research on Collective Foraging",
                    "Solving the Tower of Babel Problem: UniFysica Philo-sophia",
                    "Numinia",
                    "MathArt Conversations",
                    "Neurodivergent Learning Sessions",
                    "Draft Book: The Physics of a Fulfilling Life"
                ]
            },
            "reinference_projects": {
                "institute": [
                    "RxInfer.jl Learning and Development Group",
                    "Knowledge Engineering",
                    "Active Blockference"
                ],
                "ecosystem": [
                    "Symbolic Cognitive Robotics",
                    "Active Inference Account of Belief Updating in PTSD",
                    "Humanity's Story of an Uncertain Self",
                    "An Active Inference Agent for Modeling Human Translation Processes",
                    "Improving RxInfer.jl's Model Visualization Capabilities"
                ]
            }
        }

    def _define_board_of_directors(self):
        return [
            {"name": "John Clippinger", "statement": "I want to bring Active Inference into a broad range of applications, specifically into a new model of the firm, markets and finance."},
            {"name": "Daniel Friedman", "statement": "I expect and prefer to integrate the Institute's daily operations with our broader vision."},
            {"name": "Rafael Kaufmann", "statement": "I build adaptive sociotechnical systems that help human collectives, from teams to civilizations."},
            {"name": "Bleu Knight", "statement": "I ensure that our actions align with our values and strategic objectives, thus generating the sensations we prefer."},
            {"name": "Mike Smith", "statement": "I contribute to strategies for service and education, and facilitate epistemic foraging with active inference in commercial applications."},
            {"name": "Dean Tickles", "statement": "I see my role as a supplier of blind spot remover and a suggester of 'Escape Room' strategies as we open up active inferring."}
        ]

    def _define_scientific_advisory_board(self):
        return [
            "Mahault Albarracin", "Bradly Alicea", "Sebastian Alvarado", "John Boik",
            "Matt Brown", "John Cook", "Scott David", "Renée Davis", "Shanna Dobson",
            "Shady El Damaty", "Jeff Emmett", "Chris Fields", "Karl Friston",
            "Holly Grimm", "Avel GUÉNIN—CARLUT", "Sarah Hamburg", "Susan Hasty",
            "Conor Heins", "Susan Keen", "Thomas Kehler", "Héctor Manrique",
            "Alexandra Mikhailova", "Haris Neophytou", "Alexander Ororbia",
            "Sandeep Ramesh", "Maxwell J. D. Ramstead", "Adeel Razi",
            "Manuel Razo-Mejia", "Jakub Smekal", "Ian Tennant", "Mick Thacker",
            "Shingai Thornton", "Mark Wilcox", "Michael Zargham"
        ]

    def _define_research_fellows(self):
        return [
            {
                "name": "Anna Pereira",
                "period": "May 2024 - ",
                "project": "Cultivating a grass roots impact project (initially through nonfiction literature) to explore rapid dissemination of Active Inference Principles. Active Inference is the key lens that then expands to include human physiology and \"wellness\" concepts in the hopes of enabling humans to live more fulfilling lives, respond to increased uncertainty, and foster mutualism. The project actively provides mutualistic opportunities for collaboration and seeks to build community."
            },
            {
                "name": "Jean-Francois Cloutier",
                "period": "May 2024 - ",
                "project": "I seek to find out what it takes, at a minimum, for a robot to learn, on its own, how to survive in a world it knows initially almost nothing about. My research is the continuation of a project of many years in which I program simple autonomous robots to develop and ground my understanding of cognition. Looking for answers has already taken me on an unanticipated journey, both within and beyond Active Inference. I have been drawn into Active Inference of course but also Kantian epistemology, the issue of map vs territory, biosemiotics, mortal computing, collective intelligence, autopoiesis and constraint closure."
            },
            {
                "name": "John Boik",
                "period": "May 2024 - ",
                "project": "As an Active Inference Institute Research Fellow, the research program I will pursue is a continuation of the work I describe in a book and in two series of concept papers. That program explores the science-driven, de novo development of new cognitive architectures that are, by design, fit for purpose. The first series describes how the approach can be applied to the creation of new societal systems (e.g., new economic and governance systems), which are viewed as components of a society's cognitive architecture. The second series describes how the approach can be applied to creation of an online ecosystem that facilitates cognition in the large-group setting.",
            }
        ]
