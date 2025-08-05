import unittest
import subprocess

class TestWorkflow(unittest.TestCase):
    def test_workflow_runs(self):
        """Test if the workflow runs without errors."""
        # Try to run the main script or entry point of your package
        # Adjust the command below based on your project structure
        try:
            result = subprocess.run(
                ["python", "-m", "system_info_reader"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # Check that the process exits successfully
            self.assertEqual(result.returncode, 0, msg=f"Stdout: {result.stdout}\nStderr: {result.stderr}")
        except FileNotFoundError:
            self.fail("Could not find the entry point script for system_info_reader.")
        except Exception as e:
            self.fail(f"Exception occurred while running workflow: {e}")

if __name__ == "__main__":
    unittest.main()
