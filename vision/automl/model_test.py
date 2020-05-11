#!/usr/bin/env python

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

from google.cloud import automl_v1beta1 as automl
import pytest

project_id = os.environ["GCLOUD_PROJECT"]
compute_region = "us-central1"


@pytest.fixture
def model():
    client = automl.AutoMlClient()
    model_name = "test_" + str(uuid.uuid4())
    project_location = client.location_path(project_id, compute_region)
    my_model = {
        "display_name": model_name,
        "dataset_id": "3946265060617537378",
        "image_classification_model_metadata": {"train_budget": 24},
    }
    response = client.create_model(project_location, my_model)

    yield response

    response.cancel()


def test_model_create_status_delete(capsys, model):
    operation_name = model.operation.name
    assert operation_name