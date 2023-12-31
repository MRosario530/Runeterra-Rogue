import pygame


class Item(pygame.sprite.Sprite):   # Container class.
    def __init__(self, name, hp, attack_damage, ability_power, armor, magic_resist, cooldown_reduction, crit_chance, image, item_description):
        super().__init__()
        self.name = name
        self.image = image
        self.hp = hp
        self.attack_damage = attack_damage
        self.ability_power = ability_power
        self.armor = armor
        self.magic_resist = magic_resist
        self.cooldown_reduction = cooldown_reduction
        self.crit_chance = crit_chance
        self.item_description = item_description
