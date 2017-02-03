#!/usr/bin/env python

'''
Customization for specplot_gallery: plot a2scan with log(y) axis

This program changes the plotting for all scans that used the *a2scan* SPEC macro.
The Y axis of these plots will be plotted as logarithmic if all the data values are 
greater than zero.  Otherwise, the Y axis scale will be linear.
'''

import spec2nexus.specplot
import spec2nexus.specplot_gallery

class Custom_a2scan_Plotter(spec2nexus.specplot.LinePlotter):
    '''plot `a2scan` y axis as log if possible'''
    
    def retrieve_plot_data(self):
        '''plot the vertical axis on log scale'''
        spec2nexus.specplot.LinePlotter.retrieve_plot_data(self)

        choose_log_scale = False

        if self.signal in self.data:    # log(y) if all data positive
            choose_log_scale = min(self.data[self.signal]) > 0

        self.set_y_log(choose_log_scale)


def main():
    selector = spec2nexus.specplot.Selector()
    selector.add('a2scan', Custom_a2scan_Plotter)
    spec2nexus.specplot_gallery.main()


if __name__ == '__main__':
    # debugging_setup()
    main()

'''
Instructions:

Save this file in a directory you can write and call it from your cron tasks.  

Note that in cron entries, you cannot rely on shell environment variables to 
be defined.  Best to spell things out completely.  For example, if your $HOME 
directory is `/home/user` and you have these directories:

* `/home/user/bin`: various custom executables you use
* `/home/user/www/specplots`: a directory you access with a web browser for your plots
* `/home/user/spec/data`: a directory with your SPEC data files

then save this file to `/home/user/bin/custom_a2scan_gallery.py` and make it executable
(using `chmod +x ./home/user/bin/custom_a2scan_gallery.py`).

Edit your list of cron tasks using `crontab -e` and add this (possibly 
replacing a call to `specplot_gallery` with this call `custom_a2scan_gallery.py`)::

    # every five minutes (generates no output from outer script)
    0-59/5 * * * *  /home/user/bin/custom_a2scan_gallery.py -d /home/user/www/specplots /home/user/spec/data 2>&1 >> /home/user/www/specplots/log_cron.txt

Any output from this periodic task will be recorded in the file
`/home/user/www/specplots/log_cron.txt`.  This file can be reviewed
for diagnostics or troubleshooting.
'''
