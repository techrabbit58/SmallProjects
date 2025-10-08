import os
import sys


def clear_screen() -> None:
    clear = "cls" if sys.platform == "win32" else "clear"
    os.system(clear)


class Weapon:
    def __init__(self, name: str, damage: int) -> None:
        self.name = name
        self.damage = damage


class Character:
    def __init__(self, name: str, health: int, weapon: Weapon) -> None:
        self.name = name
        self.health = health
        self.health_max = health
        self.weapon = weapon
        print(f"{self.name} fights with {self.weapon.name}")

    def attack(self, other: "Character") -> None:
        other.health = max(other.health - self.weapon.damage, 0)
        print(f"{self.name} dealt {self.weapon.damage} damage to {other.name}")


sword = Weapon("Sword", 5)
short_bow = Weapon("Short Bow", 4)
fists = Weapon("Fists", 2)


class HealthBar:
    def __init__(self, character: Character, length: int = 25) -> None:
        self.character = character
        self.length = length

    def __str__(self) -> str:
        current_value = self.character.health
        max_value = self.character.health_max
        health = round(current_value * self.length / max_value)
        padding = self.length - health
        return (
            f"{self.character.name}'s health is {current_value}/{max_value}\n"
            f"|{'*' * health}{'_' * padding}|"
        )


class Hero(Character):
    def __init__(self, name: str, health: int) -> None:
        super().__init__(name, health, fists)
        self.default_weapon = self.weapon
        self.healh_bar = HealthBar(self)

    def take_weapon(self, weapon: Weapon) -> None:
        self.weapon = weapon
        print(f"{self.name} now fights with {weapon.name}")

    def drop_weapon(self) -> None:
        if self.weapon != self.default_weapon:
            print(f"{self.name} drops {self.weapon.name} and now fights with {self.default_weapon.name}")
            self.weapon = self.default_weapon


class Enemy(Character):
    def __init__(self, name: str, health: int) -> None:
        super().__init__(name, health, short_bow)
        self.healh_bar = HealthBar(self)


def main() -> None:
    clear_screen()
    print("T e x t   B a s e d   B a t t l e\n")
    hero = Hero("Hero", 100)
    hero.take_weapon(sword)
    print(hero.healh_bar)
    print()
    enemy = Enemy("Enemy", 100)
    print(enemy.healh_bar)
    input("\nPress Enter to continue...")

    while True:
        clear_screen()
        print("T e x t   B a s e d   B a t t l e\n")
        enemy.attack(hero)
        print(hero.healh_bar)
        print()
        hero.attack(enemy)
        print(enemy.healh_bar)

        if hero.health == 0 or enemy.health == 0:
            break

        input("\nPress Enter to continue...")

    print("\nThanks for playing.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
