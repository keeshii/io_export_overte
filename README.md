# io_export_overte

This add-on exports objects from the scene to a JSON file that is compatible with the Overte/Vircadia project.

The add-on requires Blender 3.2 or later to work. It can be used on both Windows and Linux operating systems.

## To Install

Download the whole repository as a zip file.

In the Blender: Edit > Preferences > Add-ons. Click install and select the zip file of the latest release.

Ensure the Overte add-on is checked and enabled.

## Domain URL

Before exporting a world, go to world properties and set Domain URL. It will be used as a base when building the references to other external files. Don't forget about the ending slash "/" at the end - like this "http://localhost/"

## Entities

The plugin greatly depends on the object names and maps them to the overte entities. It does not perform any vertex analisys. It also defines many new properties for the world, collections, objects and materials. Most of them have quite descriptive tooltips.

### General rule for naming objects

Object names consist of two parts separated by a dot. The first part defines the type of entity that will be exported, the next part can be anything.

For example, an object named "Image.MyImage01" will be treated as an image, and text after a dot will not be taken into account when deciding the type of object.

### Zones

Zones are exported from collections that start with "Zone". The position and size of the area will be calculated automatically based on the objects that are in this collection.

In the collection properties you can set the margin, lighting and other zone settings. The margin makes the area larger on each side by the specified number of meters.

By default the Zone is Box shaped and always axis-aligned.

### Shapes

Objects with following names will be mapped to the shape entities:

- Cube/Box -> Box Entity
- Plane -> Quad Entity
- Sphere/Icosphere -> Sphere Entity
- Cylinder -> Cylinder Entity
- Cone -> Cone Entity

Shapes will inherit the color of the first material assigned to the objects.

### Models

Objects that start with "Model" are exported to "glb" files in the subfolder of the generated "json" file. The name of the subfolder can be set in the properties of the world object.

### Models from the Asset Browser

The plugins is searching for files with extension "glb", "gltf", "fbx" or "obj" in the directories listed as "Asset Library" (Preferences > File Paths > Asset Libraries).

If the scene contains an object with the name that matches the file name (without extension), the object will be exported as model and referenced with a relative url.

In the world properties there is a button that allows you to refresh the list of models found on the disk.

### Images/Texts/Web

In order to insert an image/text/web entity, create a Plane object and rename it.

- Image -> Image Entity
- Text -> Text Entity
- Web -> Web Entity

Those entites are flat and their Z dimention will be always zero. The background color of the Text Entity will be taken from the object's material.

This type of object will only be considered if the name does not match any other type.

### Light

Add "Point" or "Spot" light to the scene and it will be exported as the light entity. Color of the light will be used as the color of the light. Othere parameters are taken from the object properties.

### Material

Materal are exported only if they are assigned to a shape entity and it's material URL is not empty.

If the same material is assigned to several shapes, it will be exported multiple times with different "parentID" values.

### Particles

Not implemented.

## Paths

You can mark places in your world by creating objects whose name starts with "Path". Information about the position and rotation of such an object will be included in the JSON file in the "Paths" section.

An object named "Path" or "Path.default" will generate an entry for the root path "/", any other name will be mapped accordingly. E.g. "Path.place" to "/place".

## Import into Overte/Vircadia

In the overte/vircadia application open the "Explorer" from the tablet and enter the path to the exported JSON file using file protocol (for example "file:///C:/world/world.json").

Or import the json file in the settings of your domain-server.




