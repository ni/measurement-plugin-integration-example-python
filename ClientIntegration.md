# Integrating Measurement Plug-Ins with User applications

You can integrate measurement plug-ins to call and execute them from user application. In this document, we will focus specifically on a **sequencer**.

## Scenario: Sequencing Measurement Plug-Ins

Imagine you have a custom application or sequencer designed to execute measurements. If you want to sequence or run measurement plug-ins using this custom application, how can you leverage it to effectively sequence and execute these measurement plug-ins?

## The Solution: Measurement Plug-In Clients

Measurement plug-in clients allow you to run measurements directly from a Python script, simplifying the process of invoking measurements from user application. [{Know more about Measurement Plug-In Client}.]({link_to_measurement_plugin_client})

The following visual illustrates how the Measurement Plug-In Client Generator can be used for calling the measurement plug-ins in user application.

![Measurement-clients-workflow](/docs/images/measurement-clients-workflow.PNG)

The steps for integrating the Measurement Plug-In Client Generator with a user application are outlined in the [Measurement Plug-In Client Integration](#example-code-to-integrate-the-measurement-plug-in-client-generator) section.

## Challenges Addressed by the Measurement Plug-In Client Generator

- The Measurement Plug-In Client Generator integrates seamlessly with custom applications and can be tailored to meet specific requirements.
- As the measure call is simple using measurement plug-in clients, it can be utilized to implement customizable sequence logic with user-defined inputs.

## Example code to Integrate the Measurement Plug-In Client Generator

- Install the Measurement Plug-In Client Generator package:

  ```bash
  pip install ni-measurement-plugin-sdk-generator
  ```

- Example usage:

  ```python
  import ni_measurement_plugin_sdk_generator.client

  args = [
      f"-s{measurement_service_class}",
      f"-o{output_directory}",
      f"-c{class_name}",
      f"-m{module_name}",
  ]
  try:
      ni_measurement_plugin_sdk_generator.client.create_client(args=args)
  except Exception as e:
      raise Exception("Exception thrown from client generation: ", e)
  ```

  This can be executed in a loop to create clients for multiple measurement plug-ins.

## Example for Integrating the Measurement Plug-In Client Generator in a User Application

For a practical implementation of this workflow, refer to our example [Sequencer tool](/README.md).
