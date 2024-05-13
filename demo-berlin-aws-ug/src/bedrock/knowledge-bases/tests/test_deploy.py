import unittest
import subprocess
import json

class TestDeploy(unittest.TestCase):
    def test_deploy_cloudformation_stack(self):
        stack_name = "MyTestStack"
        deploy_cmd = f"bash ../deploy.sh deploy_cloudformation_stack {stack_name}"
        proc = subprocess.run(deploy_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(proc.returncode, 0, f"Deploy command failed with error: {proc.stderr.decode()}")

    def test_get_stack_outputs(self):
        stack_name = "MyTestStack"
        get_outputs_cmd = f"bash ../deploy.sh get_stack_outputs {stack_name}"
        proc = subprocess.run(get_outputs_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(proc.returncode, 0, f"Get outputs command failed with error: {proc.stderr.decode()}")
        outputs = json.loads(proc.stdout.decode())
        self.assertIsNotNone(outputs.get("knowledge_base_id"))
        self.assertIsNotNone(outputs.get("vector_store_id"))
        self.assertIsNotNone(outputs.get("data_access_role_arn"))

    def test_invalid_stack_name(self):
        stack_name = "InvalidStackName"
        deploy_cmd = f"bash ../deploy.sh deploy_cloudformation_stack {stack_name}"
        proc = subprocess.run(deploy_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertNotEqual(proc.returncode, 0, "Deploy command should fail for invalid stack name")

if __name__ == "__main__":
    unittest.main()
