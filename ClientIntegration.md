# User Application Integration - {to be changed}

## The Challenge in Sequencing the Measurement Plug-Ins

Consider having an application that requires **sequence multiple measurement plug-ins**. We need a license to use TestStand in this scenario, which may not be feasible considering that we only need to sequence measurement plug-ins in a custom application. What can be the solution for this scenario? This is where the measurement plug-in clients come into the picture. It enables us to run measurements from a straightforward Python script, which can be utilized for sequencing the measurement plug-ins. [Know more about Measurement Plug-In Client]({link_to_measurement_plugin_client}).

## Need for the client creation

The primary use of the measurement plug-in client is its easy portability to user applications and its ability to be performed without the need for InstrumentStudio or TestStand. Thus, it will be appropriate for our application when it comes to the measurement plug-in sequencing.

## Client Generator Integration

{link for the client generator document}.
The steps for integrating the client generator tool with the user application have been provided in the [Client Integration](#client-integration) section.

## Gaps addressed by Client Generator

- Integration is simple.
- Enables custom sequence logic with user-defined inputs.
- Perform measurement sequencing without utilizing TestStand or InstrumentStudio.
- Easy adaptable to the user applications.
- A straightforward method calls to perform measurements as needed by the application.

## Flowchart diagram

### Sequencing using clients

![sequencing-using-clients](/docs/images/sequence-using-clients.PNG)

### Sequence workflow using the client generator

![clients-sequence-workflow](/docs/images/clients-sequence-workflow.PNG)

## Client Integration

- Install the client generator package:

```bash
pip install ni-measurement-plugin-sdk-generator`
```

- Import the module in your application:

```python
import ni_measurement_plugin_sdk_generator.client
```

- Generate the client using:

    ```python
    ni_measurement_plugin_sdk_generator.client.create_client.main(args=args)
    ```

    ***[View detailed argument specifications](link_for_argument_details_in_client_generator)***

    Accordingly, modify your arguments with respect to the options or the parameters that the method expects.
- For better error handling, wrap method calls inside try-except blocks to catch and log exceptions:

    ```python
    try:
        ni_measurement_plugin_sdk_generator.client.create_client.main(args=args)
    except Exception as e:
        print(f"Error occurred: {e}")
    ```

## Example for integrating the client generator in a sequencer

For a practical implementation of this workflow, check out our [Example sequencer tool](/README.md).
