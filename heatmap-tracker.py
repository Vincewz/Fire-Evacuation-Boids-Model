import pygame
import numpy as np
import matplotlib.pyplot as plt
from simulation import SimulationRecorder
from config import WIDTH, HEIGHT, NUM_BOIDS, ROOMS
import time
import csv
from datetime import datetime

class HeatmapSimulation(SimulationRecorder):
    def __init__(self, resolution=(200, 125)):
        super().__init__()
        self.resolution = resolution
        self.heatmap = np.zeros((resolution[1], resolution[0]))
        self.scale_x = (resolution[0] - 1) / WIDTH
        self.scale_y = (resolution[1] - 1) / HEIGHT
        self.start_time = None
        
    def get_heatmap_position(self, x, y):
        x = max(0, min(x, WIDTH))
        y = max(0, min(y, HEIGHT))
        heatmap_x = int(x * self.scale_x)
        heatmap_y = int(y * self.scale_y)
        heatmap_x = min(heatmap_x, self.resolution[0] - 1)
        heatmap_y = min(heatmap_y, self.resolution[1] - 1)
        return heatmap_x, heatmap_y
        
    def update(self):
        if not self.paused:
            super().update()
            for boid in self.boids:
                if boid.is_alive:
                    try:
                        x, y = self.get_heatmap_position(boid.position[0], boid.position[1])
                        self.heatmap[y, x] += 1
                    except IndexError as e:
                        print(f"Position error: orig_pos={boid.position}, scaled_pos=({x}, {y})")
                        print(f"Heatmap shape: {self.heatmap.shape}")
                        continue
    
    def run_with_timeout(self, timeout_seconds=240):
        running = True
        self.start_time = time.time()
        
        try:
            while running:
                current_time = time.time() - self.start_time
                if current_time > timeout_seconds:
                    print(f"Simulation timed out after {current_time:.1f} seconds")
                    break
                
                if len(self.boids) == 0 or (self.escaped_boids + self.dead_boids) >= NUM_BOIDS:
                    print(f"Simulation completed naturally after {current_time:.1f} seconds")
                    print(f"Escaped: {self.escaped_boids}, Dead: {self.dead_boids}")
                    break
                
                running = self.handle_events()
                self.update()
                self.draw()
                #self.clock.tick(60)
                
        except Exception as e:
            print(f"Simulation error: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return {
            'heatmap': self.heatmap,
            'escaped': self.escaped_boids,
            'dead': self.dead_boids,
            'time': time.time() - self.start_time
        }

def create_heatmap(resolution=(200, 125), num_runs=20, max_time=240, 
                  heatmap_output='heatmap_multi.png', stats_output='simulation_stats.csv'):
    accumulated_heatmap = np.zeros((resolution[1], resolution[0]))
    completed_runs = 0
    successful_runs = 0
    
    # Prepare stats file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stats_output = f"{stats_output.split('.')[0]}_{timestamp}.csv"
    
    with open(stats_output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Run', 'Escaped Boids', 'Dead Boids', 'Survival Rate (%)', 
                        'Simulation Time (s)', 'Status'])
        
        for run in range(num_runs):
            print(f"\nStarting simulation {run + 1}/{num_runs}")
            try:
                sim = HeatmapSimulation(resolution)
                result = sim.run_with_timeout(max_time)
                
                if result['heatmap'] is not None:
                    accumulated_heatmap += result['heatmap']
                    successful_runs += 1
                    
                    # Calculate survival rate
                    total_boids = result['escaped'] + result['dead']
                    survival_rate = (result['escaped'] / total_boids * 100) if total_boids > 0 else 0
                    
                    # Write stats to CSV
                    writer.writerow([
                        run + 1,
                        result['escaped'],
                        result['dead'],
                        f"{survival_rate:.2f}",
                        f"{result['time']:.1f}",
                        "Completed"
                    ])
                    csvfile.flush()  # Ensure data is written immediately
                
                completed_runs += 1
                
            except Exception as e:
                print(f"Run {run + 1} failed: {str(e)}")
                writer.writerow([run + 1, 'N/A', 'N/A', 'N/A', 'N/A', f"Failed: {str(e)}"])
                csvfile.flush()
            finally:
                pygame.quit()
        
        # Write summary statistics
        if successful_runs > 0:
            writer.writerow([])  # Empty row for separation
            writer.writerow(['Summary Statistics'])
            writer.writerow(['Total Runs', completed_runs])
            writer.writerow(['Successful Runs', successful_runs])
            writer.writerow(['Success Rate (%)', f"{(successful_runs/num_runs*100):.2f}"])
    
    if successful_runs > 0:
        final_heatmap = accumulated_heatmap / successful_runs
        
        # Create final visualization
        normalized = np.log1p(final_heatmap)
        normalized = (normalized - normalized.min()) / (normalized.max() - normalized.min())
        
        plt.figure(figsize=(16, 10))
        plt.imshow(normalized, cmap='hot', interpolation='gaussian', aspect='auto')
        plt.colorbar(label='Log-scaled normalized occupancy')
        plt.title(f'Boids Movement Heatmap (Average of {successful_runs} successful runs)')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        
        # Add room outlines
        scale_x = resolution[0] / WIDTH
        scale_y = resolution[1] / HEIGHT
        
        for room in ROOMS.values():
            bounds = room["bounds"]
            x, y, w, h = bounds
            x_scaled = x * scale_x
            y_scaled = y * scale_y
            w_scaled = w * scale_x
            h_scaled = h * scale_y
            plt.plot([x_scaled, x_scaled + w_scaled, x_scaled + w_scaled, x_scaled, x_scaled],
                    [y_scaled, y_scaled, y_scaled + h_scaled, y_scaled + h_scaled, y_scaled],
                    'w-', alpha=0.5)
        
        # Add timestamp to heatmap filename
        heatmap_output = f"{heatmap_output.split('.')[0]}_{timestamp}.png"
        plt.savefig(heatmap_output, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\nCompleted {completed_runs} runs, {successful_runs} successful")
        print(f"Final heatmap saved as {heatmap_output}")
        print(f"Statistics saved as {stats_output}")
    else:
        print("No successful simulations completed")

if __name__ == "__main__":
    create_heatmap(resolution=(250, 156))