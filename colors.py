import discord
import os

color_mapping = {
    (0, 100): discord.Color(int("0x3B3B3B", 16)),
    (100, 200): discord.Color(int("0xA5855E", 16)),
    (200, 300): discord.Color(int("0xCDD3D1", 16)),
    (300, 400): discord.Color(int("0xEFD862", 16)),
    (400, 500): discord.Color(int("0x3AA1B3", 16)),
    (500, 600): discord.Color(int("0xA872EE", 16)),
    (600, 700): discord.Color(int("0x389366", 16)),
    (700, float('inf')): discord.Color(int("0xB7376F", 16))
}


