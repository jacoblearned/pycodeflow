import os
import pytest
from pycodeflow.generator import Generator


class TestGenerator:
    """ Tests for the Generator Class """

    @pytest.fixture(autouse=True)
    def init_generators(self):
        self.default_generator = Generator(enabled=True)
        self.custom_generator = Generator(
            "UserInteraction", output_dir="/foo", enabled=True
        )
        self.disabled_generator = Generator()

    def test_is_enabled_default(self):
        """ _is_enabled should return False by default """
        assert self.disabled_generator.enabled is False

    def test_scenario(self):
        """ Scenario should be always have a value unless generator is disabled """
        assert self.default_generator.scenario == "Code Flow"
        assert self.custom_generator.scenario == "UserInteraction"
        assert getattr(self.disabled_generator, "scenario", None) == None

        os.environ["PYCODEFLOW_SCENARIO"] = "Environment"
        assert Generator._scenario(None) == "Environment"

    def test_paths(self):
        """ Default paths should be (<pwd>/diagrams, <pwd>/diagrams/code_flow.puml) """
        default_dir = os.path.join(os.getcwd(), "diagrams")
        default_file = os.path.join(default_dir, "code_flow.puml")
        assert self.default_generator.output_dir == default_dir
        assert self.default_generator.output_file == default_file

        assert self.custom_generator.output_dir == "/foo"
        assert self.custom_generator.output_file == "/foo/userinteraction.puml"

    @staticmethod
    @pytest.mark.parametrize(
        "enabled_value,expected_value",
        [
            ("1", True),
            ("y", True),
            ("yes", True),
            ("true", True),
            ("0", False),
            ("n", False),
            ("NO", False),
            ("false", False),
        ],
    )
    def test_is_enabled_from_env(enabled_value, expected_value):
        """ _is_enabled should return value of PYCODEFLOW_ENABLED if not explicit """

        os.environ["PYCODEFLOW_ENABLED"] = enabled_value
        assert Generator._is_enabled(None) is expected_value
