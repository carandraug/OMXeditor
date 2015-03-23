Overview
========

The OMX Editor program is a simple program for interacting with
MRC data files. Specifically, it provides the following features:

* Multi-channel image visualization
* Automatic wavelength alignment
* Image cropping

Viewing images
==============

When you run the Editor for the first time, you will be presented with
an open-file dialog. Select the MRC file you want to view, and the
program will open the file, showing you three different views of it
as well as a window with a set of parameters and histograms. In the
upper left is an XY view; below that is an XZ view and to its right is
the YZ view.

![overview](readmeFiles/overview.png)

A crosshairs pinpoints a specific pixel, which determines
which slice each view shows. You can move the crosshairs by dragging it
with the mouse, or using the numeric keypad. Press 2 and 8 to move it in
Y, 4 and 6 to move it in X, and 1 and 7 to move it in Z. You can also
move it through time using 3 and 9.

![crosshairs](readmeFiles/crosshairs.png)

Alternately, you can use the View Controls window to change how you
view the file. This window is accessible from the File menu, or by
pressing Command-T (Control-T on Windows/Linux).

![viewControls](readmeFiles/viewControls.png)

From here, you can
control which 2D views of the image are visible -- by default, you
see the XY, XZ, and YZ views, but you can also show kymographs (where
one of the image axes is time). You can also choose to show a
max-intensity projection along an axis. Finally, you can precisely set
the position of the viewing crosshairs by dragging the sliders for
each axis.

Aligning files
==============

The Editor includes an automatic adjustment algorithm to fix common
misalignments between different wavelengths of a file. It uses the
Simplex optimization algorithm to try to bring wavelengths into as much
agreement as possible, by translating, rotating, and scaling the images.
In order to obtain alignment parameters, the same image needs to be
shown in each wavelength; the best way to do this is with a test image
or bead slide. The more similar the data is in each wavelength, the
more precise the alignment will be.

![alignParams](readmeFiles/alignParams.png)

Here you can see the controls for how each wavelength is currently
transformed. X, Y, and Z translation should be self-explanatory.
Rotation is done about the Z axis, and Zoom is a uniform scaling in
X and Y.

Once you have obtained a set of alignment parameters, you can save
them to a file using the "Export parameters" button. Likewise, you can
load a previously-generated parameter set using the "Load parameters"
button. The files generated in this way can also be used by the
OMX Processor program. See later for explanations of the other buttons.

Alignment works best if the wavelengths are approximately closely
aligned to start with. You can adjust the alignment parameters manually
by typing values into the boxes (hit Enter when done), or you can
manipulate the wavelengths with the mouse. Left-click on the XY, XZ, or
YZ views and drag to translate; right-click and drag on the XY view to
rotate. You can change which wavelength(s) move by clicking on the
"Control with mouse" checkbox.

When aligning, one of the wavelengths will be held fixed, and the others
will be moved to match that wavelength as closely as possible. To change
which wavelength does not move, click on the "Use as auto-alignment
reference" radio button. Once you have everything set to your
satisfaction, click on the "Auto-align" button. A window like this
will pop up to document the alignment progress:

![alignProgress](readmeFiles/alignProgress.png)

The aligner starts with a 2D step, during which it optimizes the X and Y
translation, rotation, and zoom factors. Once it is unable to further
improve these parameters, it performs a 3D optimization using the entire
dataset to determine the optimal Z translation value. Because the 3D
step uses the entire dataset, **it is strongly recommended that you not
use very large files for alignment**. You only need enough data to
show the beads in focus and a few Z steps on either side. Including
too much data will make the 3D step take exponentially longer.

Cropping images
===============

You can use the Editor to crop images, to speed up later postprocessing
steps. The main window includes a set of parameters for cropping in X, Y,
Z, and time.

![cropParams](readmeFiles/cropParams.png)

Additionally, there is a crop box that can be manipulated with the mouse,
much like the crosshairs discussed earlier. The corners of the box start
out in the corners of the image, so it is almost invisible most of the
time. However, if you move the mouse to a corner or edge of the image,
then its cursor should change, enabling you to grab and drag the box
around.

![croppedImage](readmeFiles/croppedImage.png)

Saving changes
==============

Cropping and alignment changes are not applied to your file until you
save it (by selecting the "Save" or "Save as..." options from the File
menu). Until you do this, all operations will use the entire dataset.
Projections made with the View Controls window are never saved.

Other features
==============

The Editor includes a built-in batch-processing mode which allows you to
apply alignment and/or cropping parameters to a large number of files.

![batch](readmeFiles/batch.png)

To use this feature, first load up a file and set up its alignment
and cropping parameters the way you want them. Then click the "Batch
process" button. A dialog will pop up to let you select which of
cropping or aligning (or both) you will perform. Then you can select
which files you want to modify (hold Shift to select multiple files),
and where the modified files will be saved. Once you confirm your
selection, the batch processor will load and modify each file in turn.

The OMX Processor program is also capable of cropping and aligning files.
If you would rather use it, simply export your alignment and cropping
parameters to a file using the "Export parameters" button, then load
those parameters into the Processor's "Align and Crop" mode.

The "Dice file" button is a simple sub-feature that allows time series
image files to be split into multiple single files. This is useful for
SI timeseries data, since Priism's SI reconstruction doesn't handle
five-dimensional SI data properly. Additionally, from here you can
modify the XY and Z pixel sizes if necessary.
