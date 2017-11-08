# Stores base values like farm values and upgrade cost

# No formulas in here!


class basic:
    def __init__(self):
        # Mines
        # self.steelMineValue = 1341
        # self.noobMineValue = 985
        self.mineValues = {
            'steel': 100,
            'hydrogen': 50,
            'titanium': 250,
            'yellow crystal': 1000,
            'white crystal': 500,
            'diamond': 750,
            'silicon': 50,
            'copper': 100,
            'noobidium': 1,
            'helium': 100,
            'gold': 500,
            'liquid nitrogen': 200,
            'carbon fiber': 700,
            'oil': 20,
            'uranium': -20,
            'francium': 800,
            'lead': 10,
            'carbon': 75
        }

        self.factoryValues = {
            'Car': 3000,  # 10 steel, 1 silicon,
            'iPhoneX': 1000,  # 2 titianium, 1 copper, 2 silicon (Possible weapon license)
            'AppyLyinx': 100,  # 5 titianium, 3 copper, 3 silicon, 1 noobidium
            'Toilet': 10,  # 10 noobidium
            'Pii Fighter': 8000,
            # 50 steel, 20 titianium, 10 hydrogen, 1 white crystal, weapon lisence core, fighter license
            '4d Printer': 12000,  # 10 steel, 10 copper, 10 silicon, 1 white crystal, 1 yellow crystal
            'X128 CPU': 10000,
            'robot': 200,
            'batteries': 100,
            'plasma compressor': 6000,
            'laser': 200,
            'death star': 1000000
        }

        self.j10exs = {
            'name': 'J-10 Explorer Series',
            'desc': 'This ship is the peak of Benion engineering Being 5.3km long it is the largest ship in the '
                    'galaxy. This Ship was designed to take out any opposing fleet that went against them and so '
                    'they added a long range weapon put hungers on it and also put a range of long range weapons '
                    'on the hull. The only problem is that it is extremely slow.',
            'cost': 40000000000,
            'class': 'Super Weapon'
        }

        self.j9exs = {
            'name': 'J-9 Explorer Series',
            'desc': 'The most expensive tank there is in the Explorer Series often used as command ships.',
            'class': 'tank',
            'cost': 20000000000
        }

        self.j8exs = {
            'name': 'J-8 Explorer Series',
            'desc': 'Basically the J-9 Explorer tank but with half health.',
            'cost': 1000000000,
            'class': 'tank'
        }

        self.j7exs = {
            'name': 'J-7 Explorer Series',
            'desc': 'J-7 is a ship that carries lots of ships and brings them to combat.',
            'cost': 500000000,
            'class': 'fighter carrier'
        }

        self.j6exs = {
            'name': 'J-6 Explorer Series',
            'desc': 'Long range gun ship designed to take out ememy tanks.',
            'cost': 250000000,
            'class': 'anti tank'
        }

        self.j5exs = {
            'name': 'J-5 Explorer Series',
            'desc': 'Cheap heavy sheilded ship',
            'cost': 125000000,
            'class': 'sheilded'
        }

        self.j3exs = {
            'name': 'J-3 Explorer Series',
            'desc': 'One of the more expensive anti fighters',
            'cost': 31250000,
            'class': 'anti fighter'
        }

        self.j4exs = {
            'name': 'J-3 Explorer Series',
            'desc': 'Cheap fighter carrier',
            'cost': 62500000,
            'class': 'fighter carrier'
        }

        self.j2exs = {
            'name': 'J-2 Explorer Series',
            'desc': 'Cargo ship',
            'cost': 15625000,
            'class': 'support'
        }

        self.j1exs = {
            'name': 'J-1 Explorer Series',
            'desc': 'Troop carrier with two sections, one for boarding, one for invading',
            'cost': 7812500,
            'class': 'sheilded'
        }

        self.s10exs = {
            'name': 'S-10 Explorer Series',
            'desc': 'Most advanced fighter best suited to anti fighter',
            'cost': 3906250,
            'class': 'interceptor'
        }

        self.s9exs = {
            'name': 'S-9 Explorer Series',
            'desc': 'Fighter best suited to anti fighter',
            'cost': 1953125,
            'class': 'interceptor'
        }

        self.s8exs = {
            'name': 'S-8 Explorer Series',
            'desc': 'Fighter best suited to anti fighter',
            'cost': 976563,
            'class': 'interceptor'
        }

        self.shipDesc = {
            'j10exs': self.j10exs,
            'j9exs': self.j9exs,
            'j8exs': self.j8exs,
            'j7exs': self.j7exs,
            'j6exs': self.j6exs,
            'j5exs': self.j5exs,
            'j4exs': self.j4exs,
            'j3exs': self.j3exs,
            'j2exs': self.j2exs,
            'j1exs': self.j1exs,
            's10exs': self.s10exs,
            's9exs': self.s9exs,
            's8exs': self.s8exs,
        }  # This ship is the peak of Benion engineering Being 5.3km long it is the largest ship in the galaxy.
        # This Ship was designed to take out any opposing fleet that went against them and so they added a long range
        # weapon put hungers on it and also put a range of long range weapons on the hull.
        # The only problem is that it is extremely slow.

        self.factoryRecipies = {
            'Car': {
                'steel': 10,
                'silicon': 1
            },

            'iPhoneX': {
                'titanium': 2,
                'copper': 1,
                'silicon': 2
            },

            'AppyLyinx': {
                'titanium': 10,
                'copper': 8,
                'silicon': 8,
                'noobidium': 5
            },

            'Toilet': {
                'noobidium': 10
            },

            'Pii Fighter': {
                'steel': 2000,
                'titanium': 1000,
                'hydrogen': 200,
                'white crystal': 10
            },

            '4d Printer': {
                'steel': 1000,
                'copper': 1000,
                'silicon': 1000,
                'gold': 100,
                'white crystal': 20,
                'yellow crystal': 3
            },

            'X128 CPU': {
                'gold': 200,
                'silicon': 3000,
                'copper': 1000
            },

            'robot': {
                'gold': 4,
                'silicon': 30,
                'copper': 20,
                'titanium': 50
            },

            'batteries': {
                'lead': 5,
                'carbon': 100
            },

            'plasma compressor': {
                'titanium': 2000,
                'hydrogen': 1000,
                'oil': 2000
            },

            'laser': {
                'carbon': 200,
                'copper': 20
            },

            'death star': {
                'gold': 100000,
                'titanium': 100000,
                'yellow crystal': 500,
                'steel': 100000,
                'silicon': 200000
            }
        }

        # Farms
        self.population = 200

