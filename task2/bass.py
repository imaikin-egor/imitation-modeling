"""
Python model 'bass.py'
Translated using PySD
"""

from pathlib import Path

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.13.4"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: final_time(),
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################

@component.add(
    name="Our customers",
    units="person",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_our_customers": 1},
    other_deps={"_integ_our_customers": {"initial": {}, "step": {"our_gain": 1}}},
)
def our_customers():
    return _integ_our_customers()

_integ_our_customers = Integ(lambda: our_gain(), lambda: 0, "_integ_our_customers")

@component.add(
    name="Potential Customers",
    units="person",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_potential_customers": 1},
    other_deps={
        "_integ_potential_customers": {"initial": {}, "step": {"potential_gain": 1}}
    },
)
def potential_customers():
    return _integ_potential_customers()

_integ_potential_customers = Integ(lambda: potential_gain(), lambda: 1000000.0, "_integ_potential_customers")

@component.add(
    name="Competitor Customers",
    units="person",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_competitor_customers": 1},
    other_deps={
        "_integ_competitor_customers": {"initial": {}, "step": {"competitor_gain": 1}}
    },
)
def competitor_customers():
    return _integ_competitor_customers()

_integ_competitor_customers = Integ(lambda: competitor_gain(), lambda: 0, "_integ_competitor_customers")


@component.add(
    name="New Customers",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential2our": 1,
        "competitor2our": 1,
        "our2potential": 1,
        "our2competitor": 1
    },
)
def our_gain():
    return potential2our() + competitor2our() - our2potential() - our2competitor() 

@component.add(
    name="New Potential Customers",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "our2potential": 1,
        "competitor2potential": 1,
        "potential2our": 1,
        "potential2competitor": 1
    },
)
def potential_gain():
    return our2potential() + competitor2potential() - potential2our() - potential2competitor()

@component.add(
    name="New Competitor Customers",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential2competitor": 1,
        "our2competitor": 1,
        "competitor2potential": 1,
        "competitor2our": 1
    },
)
def competitor_gain():
    return potential2competitor() + our2competitor() - competitor2potential() - competitor2our()

@component.add(
    name="Potential Customers to Our Customers",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "our_customers": 1,
        "p11": 1,
        "sociability": 1,
        "potential_customers_concentration": 1,
        "efficiency_word_of_mouth": 1,
        "marketing_demand": 1
    },
)
def potential2our():
    satisfied_customers = our_customers() * p11()
    contacts_with_customers = satisfied_customers * sociability()
    contacts_of_noncustomers_with_customers = contacts_with_customers * potential_customers_concentration()
    word_of_mouth_demand = efficiency_word_of_mouth() * contacts_of_noncustomers_with_customers
    return marketing_demand() + word_of_mouth_demand

@component.add(
    name="Potential Customers to Competitor Customers",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "competitor_customers": 1,
        "p21": 1,
        "sociability": 1,
        "potential_customers_concentration": 1,
        "efficiency_word_of_mouth": 1,
        "marketing_demand": 1
    },
)
def potential2competitor():
    satisfied_customers = competitor_customers() * p21()
    contacts_with_customers = satisfied_customers * sociability()
    contacts_of_noncustomers_with_customers = contacts_with_customers * potential_customers_concentration()
    word_of_mouth_demand = efficiency_word_of_mouth() * contacts_of_noncustomers_with_customers
    return marketing_demand() + word_of_mouth_demand

@component.add(
    name="Our Customers to Potential Customers",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "our_customers": 1,
        "p13": 1,
        "k": 1
    },
)
def our2potential():
    return our_customers() * p13() * k()

@component.add(
    name="Competitor Customers to Potential Customers",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "competitor_customers": 1,
        "p23": 1,
        "k": 1
    },
)
def competitor2potential():
    return competitor_customers() * p23() * k()

@component.add(
    name="Our Customers to Competitor Customers",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "tr": 1,
        "efficiency_word_of_mouth": 1,
        "sociability": 1,
        "competitor_customers": 1,
        "p21": 1,
        "our_customers": 1,
        "p11": 1,
        "k": 1,
        "p13": 1,
        "total_market": 1
    },
)
def our2competitor():
    return tr() * efficiency_word_of_mouth() * sociability() * competitor_customers() * p21() * our_customers() * (1 - p11() - k() * p13()) / total_market()

@component.add(
    name="Competitor Customers to Our Customers",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "tr": 1,
        "efficiency_word_of_mouth": 1,
        "sociability": 1,
        "our_customers": 1,
        "p11": 1,
        "competitor_customers": 1,
        "p21": 1,
        "k": 1,
        "p23": 1,
        "total_market": 1
    },
)
def competitor2our():
    return tr() * efficiency_word_of_mouth() * sociability() * our_customers() * p11() * competitor_customers() * (1 - p21() - k() * p23()) / total_market()

@component.add(
    name="Demand from Marketing",
    units="person/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "efficiency_marketing": 1,
        "potential_customers": 1
    },
)
def marketing_demand():
    return efficiency_marketing() * potential_customers()

@component.add(
    name="Concentration of Potential Customers",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_customers": 1,
        "total_market": 1
    },
)
def potential_customers_concentration():
    return potential_customers() / total_market()

@component.add(
    name="Total population (actual)",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "our_customers": 1,
        "potential_customers": 1,
        "competitor_customers": 1
    },
)
def total_market():
    return our_customers() + potential_customers() + competitor_customers()

@component.add(
    name="p11",
    units="float",
    comp_type="Constant",
    comp_subtype="Normal",
)
def p11():
    return 0.5

@component.add(
    name="p13",
    units="float",
    comp_type="Constant",
    comp_subtype="Normal",
)
def p13():
    return 0.5

@component.add(
    name="p21",
    units="float",
    comp_type="Constant",
    comp_subtype="Normal",
)
def p21():
    return 0.5

@component.add(
    name="p23",
    units="float",
    comp_type="Constant",
    comp_subtype="Normal",
)
def p23():
    return 0.5

@component.add(
    name="Word of Mouth impact",
    units="person/contact",
    comp_type="Constant",
    comp_subtype="Normal",
)
def efficiency_word_of_mouth():
    return 0.015

@component.add(
    name="Marketing impact",
    units="person/contact",
    comp_type="Constant",
    comp_subtype="Normal",
)
def efficiency_marketing():
    return 0.01

@component.add(
    name="FINAL TIME",
    units="int",
    comp_type="Constant",
    comp_subtype="Normal",
)
def final_time():
    return 1000

@component.add(
    name="Rate",
    units="contact/person/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sociability():
    return 100

@component.add(
    name="k",
    units="float",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "efficiency_marketing": 1,
        "efficiency_word_of_mouth": 1
    },
)
def k():
    return 2 * efficiency_marketing() / (2 * efficiency_marketing() + 2 * efficiency_word_of_mouth())


@component.add(
    name="tr",
    units="float",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "efficiency_word_of_mouth": 1,
        "efficiency_marketing": 1
    },
)
def tr():
    return 2 * efficiency_word_of_mouth() / (2 * efficiency_marketing() + 2 * efficiency_word_of_mouth())
