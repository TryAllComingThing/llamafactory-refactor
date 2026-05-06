<template>
  <div class="loss-chart-wrapper">
    <div v-if="data.length === 0" class="loss-chart-empty">{{ $t('no_training_data') }}</div>
    <div ref="chartRef" class="loss-chart" :class="{ 'loss-chart--hidden': data.length === 0 }" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue";
import * as echarts from "echarts";

interface LossPoint {
  step: number;
  value: number;
}

const props = withDefaults(
  defineProps<{
    data?: LossPoint[];
  }>(),
  { data: () => [] },
);

const chartRef = ref<HTMLElement | null>(null);
let chart: echarts.ECharts | null = null;
const resizeHandler = () => chart?.resize();

function initChart(): void {
  if (!chartRef.value || props.data.length === 0) return;
  chart = echarts.init(chartRef.value);
  updateChart();
}

function updateChart(): void {
  if (!chart) return;
  chart.setOption({
    tooltip: {
      trigger: "axis",
      formatter: (params: Array<{ axisValueLabel: string; value: number }>) => {
        const p = params[0];
        if (!p) return "";
        return `Step ${p.axisValueLabel}<br/>Loss: ${p.value.toFixed(6)}`;
      },
    },
    grid: { left: 50, right: 20, top: 20, bottom: 30 },
    xAxis: {
      type: "value",
      name: "Step",
      min: 0,
    },
    yAxis: {
      type: "value",
      name: "Loss",
      min: 0,
    },
    series: [
      {
        type: "line",
        data: props.data.map((d) => [d.step, d.value]),
        smooth: true,
        showSymbol: false,
        lineStyle: { width: 2 },
        areaStyle: {
          opacity: 0.1,
        },
      },
    ],
    animation: false,
  });
}

watch(
  () => props.data,
  () => {
    if (!chart && props.data.length > 0) initChart();
    else updateChart();
  },
  { deep: true },
);

onMounted(() => {
  initChart();
  window.addEventListener("resize", resizeHandler);
});

onUnmounted(() => {
  window.removeEventListener("resize", resizeHandler);
  chart?.dispose();
});
</script>

<style scoped>
.loss-chart-wrapper {
  position: relative;
}

.loss-chart {
  width: 100%;
  height: 300px;
}

.loss-chart--hidden {
  visibility: hidden;
  height: 0;
}

.loss-chart-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: var(--text-tertiary);
  font-size: var(--font-size-sm);
}
</style>
