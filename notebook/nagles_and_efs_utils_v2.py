#!/usr/bin/env python
# coding: utf-8

# In[69]:


import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter, HourLocator
from pytz import timezone
from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource, Range1d, LinearAxis, Span, DatetimeTickFormatter, BasicTicker

output_notebook()


# In[70]:


# Import CSV data
write_benchmarks_v2_0_0 = pd.read_csv('bench_writes_v2_0_0.csv')
write_benchmarks_v2_0_1 = pd.read_csv('bench_writes_v2_0_1.csv')


# In[71]:


# Clean up timestamps
def clean_timestamps(df):
    df['human_time'] = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f") for t in df['timestamp']]
    df['human_time'] = [ts.tz_localize('UTC') for ts in df['human_time']]
    
clean_timestamps(write_benchmarks_v2_0_0)
clean_timestamps(write_benchmarks_v2_0_1)


# In[72]:


# Add ms columns
def add_ms_latencies(df):
    df['latency_ms'] = [lat / 1000 for lat in df['latency_us']]
    
add_ms_latencies(write_benchmarks_v2_0_0)
add_ms_latencies(write_benchmarks_v2_0_1)


# In[73]:


def plot_write_benchmark(write_benchmark, graph_title, io_size):

    p = figure(
            title=graph_title, 
            x_axis_label="Time from start of test (:min:sec)", 
            y_axis_label="Latency (ms)", 
            x_axis_type="datetime",
            width=900, height=700
        )

    p.xaxis.ticker = BasicTicker(desired_num_ticks=15)
    p.yaxis.ticker = BasicTicker(desired_num_ticks=15)
    
    proxy_bench = write_benchmark[
        (write_benchmark["mount_type"] == "efs-proxy") &
        (write_benchmark["io_size"] == io_size)
    ]
    stunnel_bench = write_benchmark[
        (write_benchmark["mount_type"] == "stunnel") &
        (write_benchmark["io_size"] == io_size)
    ]
    
    p.scatter(x="human_time", y="latency_ms", legend_label="efs-proxy", source=proxy_bench, color="blue", size=6)
    p.scatter(x="human_time", y="latency_ms", legend_label="stunnel", source=stunnel_bench, color="red", size=6)

    p.legend.location = "top_left"
    p.legend.click_policy="mute"

    show(p)


# In[74]:


plot_write_benchmark(write_benchmarks_v2_0_0, "stunnel and efs-proxy latencies for 1 KB writes", 1024)
plot_write_benchmark(write_benchmarks_v2_0_0, "stunnel and efs-proxy latencies for 9 KB writes", 9216)


# In[ ]:




