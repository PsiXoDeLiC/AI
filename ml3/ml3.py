import sqlite3
from enum import Enum
import numpy as np

class MaterialProperty(Enum):
    ALUMINUM = "Алюминий"
    STEEL = "Сталь" 
    TITANIUM = "Титан"
    COPPER = "Медь"
    PLASTIC = "Пластик"

class FuzzySystem:
    """Система нечеткой логики с фаззификацией и дефаззификацией"""
    
    @staticmethod
    def fuzzify_hardness(hardness):
        """Фаззификация твердости материала"""
        print(f"\n ФАЗЗИФИКАЦИЯ ТВЕРДОСТИ: {hardness} HB")
        
        # Нечеткие множества для твердости
        soft = max(0, min(1, (4 - hardness) / 2)) if hardness <= 4 else 0
        medium = max(0, min(1, (hardness - 2) / 2, (8 - hardness) / 2)) if 2 <= hardness <= 8 else 0
        hard = max(0, min(1, (hardness - 6) / 2)) if hardness >= 6 else 0
        
        print(f"   Мягкий: {soft:.2f}")
        print(f"   Средний: {medium:.2f}") 
        print(f"   Твердый: {hard:.2f}")
        
        return {'soft': soft, 'medium': medium, 'hard': hard}
    
    @staticmethod
    def fuzzify_strength(strength):
        """Фаззификация прочности материала"""
        print(f"\n ФАЗЗИФИКАЦИЯ ПРОЧНОСТИ: {strength} МПа")
        
        low = max(0, min(1, (200 - strength) / 150)) if strength <= 200 else 0
        medium = max(0, min(1, (strength - 100) / 150, (400 - strength) / 150)) if 100 <= strength <= 400 else 0
        high = max(0, min(1, (strength - 300) / 200)) if strength >= 300 else 0
        
        print(f"   Низкая: {low:.2f}")
        print(f"   Средняя: {medium:.2f}")
        print(f"   Высокая: {high:.2f}")
        
        return {'low': low, 'medium': medium, 'high': high}
    
    @staticmethod
    def fuzzify_thermal_conductivity(thermal):
        """Фаззификация теплопроводности"""
        print(f"\n ФАЗЗИФИКАЦИЯ ТЕПЛОПРОВОДНОСТИ: {thermal} Вт/(м·K)")
        
        low = max(0, min(1, (50 - thermal) / 40)) if thermal <= 50 else 0
        medium = max(0, min(1, (thermal - 30) / 40, (150 - thermal) / 100)) if 30 <= thermal <= 150 else 0
        high = max(0, min(1, (thermal - 100) / 150)) if thermal >= 100 else 0
        
        print(f"   Низкая: {low:.2f}")
        print(f"   Средняя: {medium:.2f}")
        print(f"   Высокая: {high:.2f}")
        
        return {'low': low, 'medium': medium, 'high': high}
    
    @staticmethod
    def apply_rules(hardness_fuzzy, strength_fuzzy, thermal_fuzzy):
        """Применение нечетких правил"""
        print(f"\n ПРИМЕНЕНИЕ НЕЧЕТКИХ ПРАВИЛ:")
        print("=" * 50)
        
        # Инициализация выходных нечетких множеств
        speed_fuzzy = {'slow': 0, 'medium': 0, 'fast': 0}
        feed_fuzzy = {'slow': 0, 'medium': 0, 'fast': 0}
        cooling_fuzzy = {'low': 0, 'medium': 0, 'high': 0}
        
        # ПРАВИЛО 1: Если материал твердый, то скорость медленная
        rule1_activation = hardness_fuzzy['hard']
        speed_fuzzy['slow'] = max(speed_fuzzy['slow'], rule1_activation)
        print(f" ПРАВИЛО 1: ЕСЛИ твердый ({hardness_fuzzy['hard']:.2f}) ТОГДА скорость медленная")
        print(f"   → Активация медленной скорости: {rule1_activation:.2f}")
        
        # ПРАВИЛО 2: Если материал мягкий, то скорость быстрая
        rule2_activation = hardness_fuzzy['soft']
        speed_fuzzy['fast'] = max(speed_fuzzy['fast'], rule2_activation)
        print(f" ПРАВИЛО 2: ЕСЛИ мягкий ({hardness_fuzzy['soft']:.2f}) ТОГДА скорость быстрая")
        print(f"   → Активация быстрой скорости: {rule2_activation:.2f}")
        
        # ПРАВИЛО 3: Если материал средней твердости, то скорость средняя
        rule3_activation = hardness_fuzzy['medium']
        speed_fuzzy['medium'] = max(speed_fuzzy['medium'], rule3_activation)
        print(f" ПРАВИЛО 3: ЕСЛИ средний ({hardness_fuzzy['medium']:.2f}) ТОГДА скорость средняя")
        print(f"   → Активация средней скорости: {rule3_activation:.2f}")
        
        # ПРАВИЛО 4: Если прочность высокая, то подача медленная
        rule4_activation = strength_fuzzy['high']
        feed_fuzzy['slow'] = max(feed_fuzzy['slow'], rule4_activation)
        print(f" ПРАВИЛО 4: ЕСЛИ прочность высокая ({strength_fuzzy['high']:.2f}) ТОГДА подача медленная")
        print(f"   → Активация медленной подачи: {rule4_activation:.2f}")
        
        # ПРАВИЛО 5: Если прочность низкая, то подача быстрая
        rule5_activation = strength_fuzzy['low']
        feed_fuzzy['fast'] = max(feed_fuzzy['fast'], rule5_activation)
        print(f" ПРАВИЛО 5: ЕСЛИ прочность низкая ({strength_fuzzy['low']:.2f}) ТОГДА подача быстрая")
        print(f"   → Активация быстрой подачи: {rule5_activation:.2f}")
        
        # ПРАВИЛО 6: Если теплопроводность низкая, то охлаждение сильное
        rule6_activation = thermal_fuzzy['low']
        cooling_fuzzy['high'] = max(cooling_fuzzy['high'], rule6_activation)
        print(f"  ПРАВИЛО 6: ЕСЛИ теплопроводность низкая ({thermal_fuzzy['low']:.2f}) ТОГДА охлаждение сильное")
        print(f"   → Активация сильного охлаждения: {rule6_activation:.2f}")
        
        # ПРАВИЛО 7: Если теплопроводность высокая, то охлаждение слабое
        rule7_activation = thermal_fuzzy['high']
        cooling_fuzzy['low'] = max(cooling_fuzzy['low'], rule7_activation)
        print(f"  ПРАВИЛО 7: ЕСЛИ теплопроводность высокая ({thermal_fuzzy['high']:.2f}) ТОГДА охлаждение слабое")
        print(f"   → Активация слабого охлаждения: {rule7_activation:.2f}")
        
        print(f"\n НЕЧЕТКИЕ ВЫХОДНЫЕ МНОЖЕСТВА:")
        print(f"   Скорость: медленная={speed_fuzzy['slow']:.2f}, средняя={speed_fuzzy['medium']:.2f}, быстрая={speed_fuzzy['fast']:.2f}")
        print(f"   Подача: медленная={feed_fuzzy['slow']:.2f}, средняя={feed_fuzzy['medium']:.2f}, быстрая={feed_fuzzy['fast']:.2f}")
        print(f"   Охлаждение: слабое={cooling_fuzzy['low']:.2f}, среднее={cooling_fuzzy['medium']:.2f}, сильное={cooling_fuzzy['high']:.2f}")
        
        return speed_fuzzy, feed_fuzzy, cooling_fuzzy
    
    @staticmethod
    def defuzzify_speed(speed_fuzzy):
        """Дефаззификация скорости резания"""
        print(f"\n🔧 ДЕФАЗЗИФИКАЦИЯ СКОРОСТИ:")
        
        # Определения нечетких множеств для скорости (об/мин)
        slow_range = (500, 1000, 1500)    # треугольник: 500-1500, пик на 1000
        medium_range = (1000, 2000, 3000) # треугольник: 1000-3000, пик на 2000  
        fast_range = (2000, 3500, 5000)   # треугольник: 2000-5000, пик на 3500
        
        # Метод центра тяжести (Centroid)
        numerator = 0
        denominator = 0
        
        # Генерируем точки для расчета
        x_values = np.linspace(500, 5000, 100)
        
        for x in x_values:
            # Вычисляем степень принадлежности для каждого x
            mu_slow = max(0, min(1, (x - slow_range[0]) / (slow_range[1] - slow_range[0]), 
                              (slow_range[2] - x) / (slow_range[2] - slow_range[1]))) if slow_range[0] <= x <= slow_range[2] else 0
            
            mu_medium = max(0, min(1, (x - medium_range[0]) / (medium_range[1] - medium_range[0]), 
                                (medium_range[2] - x) / (medium_range[2] - medium_range[1]))) if medium_range[0] <= x <= medium_range[2] else 0
            
            mu_fast = max(0, min(1, (x - fast_range[0]) / (fast_range[1] - fast_range[0]), 
                               (fast_range[2] - x) / (fast_range[2] - fast_range[1]))) if fast_range[0] <= x <= fast_range[2] else 0
            
            # Объединяем выходные нечеткие множества (метод максимума)
            mu_output = max(
                min(mu_slow, speed_fuzzy['slow']),
                min(mu_medium, speed_fuzzy['medium']), 
                min(mu_fast, speed_fuzzy['fast'])
            )
            
            numerator += x * mu_output
            denominator += mu_output
        
        speed = numerator / denominator if denominator > 0 else 2000
        
        print(f"   Медленная: {speed_fuzzy['slow']:.2f} → диапазон 500-1500 об/мин")
        print(f"   Средняя: {speed_fuzzy['medium']:.2f} → диапазон 1000-3000 об/мин")
        print(f"   Быстрая: {speed_fuzzy['fast']:.2f} → диапазон 2000-5000 об/мин")
        print(f"   → Рассчитанная скорость: {speed:.0f} об/мин")
        
        return round(speed)
    
    @staticmethod
    def defuzzify_feed(feed_fuzzy):
        """Дефаззификация подачи"""
        print(f"\n ДЕФАЗЗИФИКАЦИЯ ПОДАЧИ:")
        
        # Определения нечетких множеств для подачи (мм/об)
        slow_range = (0.05, 0.1, 0.2)    # треугольник: 0.05-0.2, пик на 0.1
        medium_range = (0.1, 0.3, 0.5)   # треугольник: 0.1-0.5, пик на 0.3
        fast_range = (0.3, 0.6, 1.0)     # треугольник: 0.3-1.0, пик на 0.6
        
        numerator = 0
        denominator = 0
        
        x_values = np.linspace(0.05, 1.0, 100)
        
        for x in x_values:
            mu_slow = max(0, min(1, (x - slow_range[0]) / (slow_range[1] - slow_range[0]), 
                              (slow_range[2] - x) / (slow_range[2] - slow_range[1]))) if slow_range[0] <= x <= slow_range[2] else 0
            
            mu_medium = max(0, min(1, (x - medium_range[0]) / (medium_range[1] - medium_range[0]), 
                                (medium_range[2] - x) / (medium_range[2] - medium_range[1]))) if medium_range[0] <= x <= medium_range[2] else 0
            
            mu_fast = max(0, min(1, (x - fast_range[0]) / (fast_range[1] - fast_range[0]), 
                               (fast_range[2] - x) / (fast_range[2] - fast_range[1]))) if fast_range[0] <= x <= fast_range[2] else 0
            
            mu_output = max(
                min(mu_slow, feed_fuzzy['slow']),
                min(mu_medium, feed_fuzzy['medium']),
                min(mu_fast, feed_fuzzy['fast'])
            )
            
            numerator += x * mu_output
            denominator += mu_output
        
        feed = numerator / denominator if denominator > 0 else 0.2
        
        print(f"   Медленная: {feed_fuzzy['slow']:.2f} → диапазон 0.05-0.2 мм/об")
        print(f"   Средняя: {feed_fuzzy['medium']:.2f} → диапазон 0.1-0.5 мм/об") 
        print(f"   Быстрая: {feed_fuzzy['fast']:.2f} → диапазон 0.3-1.0 мм/об")
        print(f"   → Рассчитанная подача: {feed:.3f} мм/об")
        
        return round(feed, 3)
    
    @staticmethod
    def defuzzify_cooling(cooling_fuzzy):
        """Дефаззификация охлаждения"""
        print(f"\n ДЕФАЗЗИФИКАЦИЯ ОХЛАЖДЕНИЯ:")
        
        # Определения нечетких множеств для охлаждения (%)
        low_range = (0, 20, 40)      # треугольник: 0-40, пик на 20
        medium_range = (30, 50, 70)  # треугольник: 30-70, пик на 50  
        high_range = (60, 80, 100)   # треугольник: 60-100, пик на 80
        
        numerator = 0
        denominator = 0
        
        x_values = np.linspace(0, 100, 100)
        
        for x in x_values:
            mu_low = max(0, min(1, (x - low_range[0]) / (low_range[1] - low_range[0]), 
                             (low_range[2] - x) / (low_range[2] - low_range[1]))) if low_range[0] <= x <= low_range[2] else 0
            
            mu_medium = max(0, min(1, (x - medium_range[0]) / (medium_range[1] - medium_range[0]), 
                               (medium_range[2] - x) / (medium_range[2] - medium_range[1]))) if medium_range[0] <= x <= medium_range[2] else 0
            
            mu_high = max(0, min(1, (x - high_range[0]) / (high_range[1] - high_range[0]), 
                              (high_range[2] - x) / (high_range[2] - high_range[1]))) if high_range[0] <= x <= high_range[2] else 0
            
            mu_output = max(
                min(mu_low, cooling_fuzzy['low']),
                min(mu_medium, cooling_fuzzy['medium']),
                min(mu_high, cooling_fuzzy['high'])
            )
            
            numerator += x * mu_output
            denominator += mu_output
        
        cooling = numerator / denominator if denominator > 0 else 50
        
        print(f"   Слабое: {cooling_fuzzy['low']:.2f} → диапазон 0-40%")
        print(f"   Среднее: {cooling_fuzzy['medium']:.2f} → диапазон 30-70%")
        print(f"   Сильное: {cooling_fuzzy['high']:.2f} → диапазон 60-100%")
        print(f"   → Рассчитанное охлаждение: {cooling:.0f}%")
        
        return round(cooling)

class MachineParameters:
    """Расчет параметров станка с использованием нечеткой логики"""
    
    MATERIAL_PROPERTIES = {
        MaterialProperty.ALUMINUM: {
            'hardness': 2.5, 'density': 2.7, 'thermal_conductivity': 237,
            'tensile_strength': 90, 'machinability': 0.8,
        },
        MaterialProperty.STEEL: {
            'hardness': 6.0, 'density': 7.8, 'thermal_conductivity': 50,
            'tensile_strength': 500, 'machinability': 0.5,
        },
        MaterialProperty.TITANIUM: {
            'hardness': 8.5, 'density': 4.5, 'thermal_conductivity': 22,
            'tensile_strength': 900, 'machinability': 0.3,
        },
        MaterialProperty.COPPER: {
            'hardness': 3.0, 'density': 8.9, 'thermal_conductivity': 401,
            'tensile_strength': 210, 'machinability': 0.7,
        },
        MaterialProperty.PLASTIC: {
            'hardness': 1.5, 'density': 1.2, 'thermal_conductivity': 0.2,
            'tensile_strength': 50, 'machinability': 0.9,
        }
    }
    
    @classmethod
    def calculate_parameters(cls, material_type):
        """Расчет параметров через нечеткую логику"""
        props = cls.MATERIAL_PROPERTIES[material_type]
        
        print(f" РАСЧЕТ ПАРАМЕТРОВ ДЛЯ {material_type.value}")
        print("=" * 60)
        
        # 1. ФАЗЗИФИКАЦИЯ - преобразование четких значений в нечеткие
        hardness_fuzzy = FuzzySystem.fuzzify_hardness(props['hardness'])
        strength_fuzzy = FuzzySystem.fuzzify_strength(props['tensile_strength'])
        thermal_fuzzy = FuzzySystem.fuzzify_thermal_conductivity(props['thermal_conductivity'])
        
        # 2. ПРИМЕНЕНИЕ ПРАВИЛ - нечеткий вывод
        speed_fuzzy, feed_fuzzy, cooling_fuzzy = FuzzySystem.apply_rules(
            hardness_fuzzy, strength_fuzzy, thermal_fuzzy
        )
        
        # 3. ДЕФАЗЗИФИКАЦИЯ - преобразование нечетких значений в четкие
        cutting_speed = FuzzySystem.defuzzify_speed(speed_fuzzy)
        feed_rate = FuzzySystem.defuzzify_feed(feed_fuzzy)
        cooling_flow = FuzzySystem.defuzzify_cooling(cooling_fuzzy)
        
        # Расчет мощности на основе четких значений
        spindle_power = cls._calculate_power(props, cutting_speed, feed_rate)
        
        return {
            'material': material_type.value,
            'cutting_speed': cutting_speed,
            'feed_rate': feed_rate,
            'cooling_flow': cooling_flow,
            'spindle_power': spindle_power,
        }
    
    @classmethod
    def _calculate_power(cls, props, speed, feed):
        """Расчет мощности шпинделя"""
        power = props['hardness'] * speed * feed / 1000
        return round(max(1.0, power), 1)

class MachineController:
    """Управление промышленным станком"""
    
    def __init__(self, machine_id="CNC_001"):
        self.machine_id = machine_id
        self.current_parameters = None
    
    def load_material(self, material_type):
        """Загрузка материала и расчет параметров"""
        print(f"\n СТАНОК {self.machine_id}: ЗАГРУЗКА {material_type.value}")
        
        self.current_parameters = MachineParameters.calculate_parameters(material_type)
        
        print(f"\n РАСЧЕТ ЗАВЕРШЕН!")
        self._display_final_parameters()
        
        return self.current_parameters
    
    def _display_final_parameters(self):
        """Отображение финальных параметров"""
        params = self.current_parameters
        
        print(f"\n ФИНАЛЬНЫЕ ПАРАМЕТРЫ ОБРАБОТКИ:")
        print(f"    Скорость резания: {params['cutting_speed']} об/мин")
        print(f"    Подача: {params['feed_rate']} мм/об")
        print(f"    Охлаждение: {params['cooling_flow']}%")
        print(f"    Мощность шпинделя: {params['spindle_power']} кВт")

def main():
    """Главная функция - демонстрация работы системы"""
    print(" СИСТЕМА АВТОМАТИЗАЦИИ СТАНКОВ С НЕЧЕТКОЙ ЛОГИКОЙ")
    print("=" * 60)
    
    machine = MachineController("CNC_001")
    
    # Демонстрационные сценарии
    scenarios = [
        MaterialProperty.ALUMINUM,
        MaterialProperty.STEEL, 
        MaterialProperty.TITANIUM,
    ]
    
    for material in scenarios:
        print(f"\n{'#' * 60}")
        print(f"#{' СЦЕНАРИЙ: ' + material.value + ' ':#<47}#")
        print(f"{'#' * 60}")
        
        machine.load_material(material)
        input("\nНажмите Enter для следующего сценария...")
    
    print(f"\n ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")

if __name__ == "__main__":
    main()