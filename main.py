import graph
import fuzzy_logic_system as fs

##################################
###  LIE - DETECTION - SYSTEM  ###
##################################

##########################
# <PrepositionsVariables>
##########################

# region Degree of Credibility (appreciation)
dc_credible = fs.TrapezoidalFuzzySet('credible', domain=(0, 10))
degree_of_credibility = fs.LanguageVariable(
    'Credibility',
    dc_credible
)
# endregion

# region Heart Rate (BEATS/MINUTES)
hr_slow = fs.LFuzzySet('slow', domain=(0, 70))
hr_medium = fs.TrapezoidalFuzzySet('medium', domain=(55, 120))
hr_fast = fs.GammaFuzzySet('fast', domain=(110, 180))
heart_rate = fs.LanguageVariable(
    'HeartRate',
    hr_fast,
    hr_medium,
    hr_slow
)

# endregion

# region Blood Systolic Pressure (mmHg)
bsp_normal = fs.ZFuzzySet('normal', domain=(0, 120))
bsp_slightly_high = fs.GaussianFuzzySet('slightly-high', domain=(110, 140))
bsp_high = fs.SigmoidalFuzzySet('high', domain=(130, 180))
blood_systolic_pressure = fs.LanguageVariable(
    'BloodSystolicPressure',
    bsp_normal,
    bsp_slightly_high,
    bsp_high
)

# endregion

# region Blood Diastolic Pressure (mmHg)
bdp_normal = fs.ZFuzzySet('normal', domain=(0, 90))
bdp_slightly_high = fs.GaussianFuzzySet('slightly-high', domain=(75, 95))
bdp_high = fs.SigmoidalFuzzySet('high', domain=(90, 110))
blood_diastolic_pressure = fs.LanguageVariable(
    'BloodDiastolicPressure',
    bdp_normal,
    bdp_slightly_high,
    bdp_high
)

# endregion

# region Breathing Speed
bs_decreasing = fs.ZFuzzySet('decreasing', domain=(-10, 0))
bs_constant = fs.GaussianFuzzySet('constant', domain=(-2, 2))
bs_increasing = fs.SigmoidalFuzzySet('increasing', domain=(0, 10))
breathing_speed = fs.LanguageVariable(
    'BreathingSpeed',
    bs_decreasing,
    bs_constant,
    bs_increasing
)

# endregion

# region Skin Conductance (relating with the sweat)
sc_normal = fs.ZFuzzySet('normal', domain=(0, 10))
sc_high = fs.SigmoidalFuzzySet('high', domain=(8, 20))
skin_conductance = fs.LanguageVariable(
    'SkinConductance',
    sc_normal,
    sc_high
)

# endregion

#########################
# <ConsequentVariables>
#########################

# region Stress Level
strs_low = fs.ZFuzzySet('low', domain=(0, 4.5))
strs_medium = fs.GaussianFuzzySet('medium', domain=(3, 7))
strs_high = fs.SigmoidalFuzzySet('high', domain=(5.5, 10))
stress_level = fs.LanguageVariable(
    'StressLevel',
    strs_low,
    strs_medium,
    strs_high
)

# endregion

# region Veredict
v_lying = fs.ZFuzzySet('lying', domain=(0, 5.5))
v_confessing = fs.SigmoidalFuzzySet('confessing', domain=(4.5, 10))
veredict = fs.LanguageVariable(
    'Veredict',
    v_lying,
    v_confessing
)

# endregion

#########################
# <Propositions-Alias>
#########################

# region Blood Pressure Prepositions
proposition_stable_blood_pressure = (
    (blood_diastolic_pressure % 'normal') &
    (blood_systolic_pressure % 'normal')
)
proposition_slightly_high_blood_pressure = (
    (blood_diastolic_pressure % 'slightly-high') &
    (blood_systolic_pressure % 'slightly-high') |

    (blood_diastolic_pressure % 'slightly-high') &
    (blood_systolic_pressure % 'normal') |

    (blood_diastolic_pressure % 'normal') &
    (blood_systolic_pressure % 'slightly-high')
)
proposition_high_blood_pressure = (
    (blood_diastolic_pressure % 'high') &
    (blood_systolic_pressure % 'high') |

    (blood_diastolic_pressure % 'high') &
    (blood_systolic_pressure % 'slightly-high') |

    (blood_diastolic_pressure % 'slightly-high') &
    (blood_systolic_pressure % 'high')
)

# endregion

# region Credibility Prepositions
proposition_credible = (degree_of_credibility % 'credible')
proposition_not_credible = ~(degree_of_credibility % 'credible')

# endregion

#########################
# <Rules>
#########################

# region Rules
rule1 = fs.MamdaniRule(
    (
        (heart_rate % 'fast') |
        (breathing_speed % 'increasing') |
        (skin_conductance % 'high')
    ), [
        (stress_level, 'high'),
        (veredict, 'lying')
    ]
)
rule2 = fs.MamdaniRule(
    (
        (heart_rate % 'slow') |
        (breathing_speed % 'decreasing')
    ) & (skin_conductance % 'normal'),
    [
        (stress_level, 'low')
    ]
)
rule3 = fs.MamdaniRule(
    proposition_stable_blood_pressure,
    [
        (stress_level, 'low'),
        (veredict, 'confessing')
    ]
)
rule4 = fs.MamdaniRule(
    proposition_high_blood_pressure |
    proposition_slightly_high_blood_pressure,
    [
        (stress_level, 'medium'),
    ]
)
rule5 = fs.MamdaniRule(
    proposition_high_blood_pressure,
    [
        (stress_level, 'medium'),
        (veredict, 'lying'),
    ]
)
rule6 = fs.MamdaniRule(
    (
        (heart_rate % 'fast') |
        (breathing_speed % 'increasing') |
        (skin_conductance % 'high')
    ),
    [
        (stress_level, 'medium'),
        (veredict, 'lying')
    ]
)
rule7 = fs.MamdaniRule(
    (
        (heart_rate % 'medium') |
        (breathing_speed % 'constant') |
        (skin_conductance % 'normal')
    ) & proposition_credible,
    [
        (stress_level, 'medium'),
        (veredict, 'confessing')
    ]
)
rule8 = fs.MamdaniRule(
    (
        (heart_rate % 'slow') |
        (breathing_speed % 'decreasing') |
        (skin_conductance % 'normal')
    ),
    [
        (stress_level, 'low'),
        (veredict, 'confessing')
    ]
)
rule9 = fs.MamdaniRule(
    proposition_credible,
    [
        (veredict, 'confessing')
    ]
)
rule10 = fs.MamdaniRule(
    proposition_not_credible,
    [
        (veredict, 'lying')
    ]
)
fuzzy_inference_system = fs.fuzzy_system_impl.FuzzyInferenceSystem(
    rules=[rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9]
)

# endregion

#########################
# <Inputs>
#########################

# region I/O
print('-' * 50)
print('\tVALUES:')
credibility_value = float(
    input('Degree of Credibility (appreciation) [0, 10]: ')
)
heart_rate_value = float(
    input('Heart Rate (BEATS/MINUTES) [0, 180]: ')
)
blood_systolic_pressure_value = float(
    input('Blood Systolic Pressure (mmHg) [0, 180]: ')
)
blood_diastolic_pressure_value = float(
    input('Blood Diastolic Pressure (mmHg) [0, 110]: ')
)
breathing_speed_value = float(
    input('Breathing Speed (BEATS/MINUTES) [-10, 10]: ')
)
skin_conductance_value = float(
    input('Skin Conductance (relating with the sweat) [0, 20]: ')
)

# endregion

#########################
# <Inference>
#########################

# region Inference
infered = fuzzy_inference_system.infer({
    'Credibility': credibility_value,
    'HeartRate': heart_rate_value,
    'BloodSystolicPressure': blood_systolic_pressure_value,
    'BloodDiastolicPressure': blood_diastolic_pressure_value,
    'BreathingSpeed': breathing_speed_value,
    'SkinConductance': skin_conductance_value,
})
# endregion

# region Answers
print('-' * 50)
print('\tCONCLUSIONS:')
print('StressLevel: %.2f / 10' % infered['StressLevel'])
print('Veredict:    %.2f / 10' % infered['Veredict'])

# endregion
