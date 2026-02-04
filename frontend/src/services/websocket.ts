interface WebSocketMessage {
  type: 'price_update' | 'trade_update' | 'system_message';
  data: any;
  timestamp: string;
}

interface PriceUpdateData {
  price_per_gram: number;
  price_per_baht: number;
  currency: string;
  timestamp: string;
  change_24h?: number;
  change_percent_24h?: number;
  volume_24h?: number;
}

interface TradeUpdateData {
  transaction_id: number;
  user_id: number;
  transaction_type: 'BUY' | 'SELL';
  gold_weight: number;
  gold_price_per_gram: number;
  total_amount: number;
  status: 'PENDING' | 'COMPLETED' | 'CANCELLED';
  timestamp: string;
}

class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private url: string;
  private subscriptions: Set<string> = new Set();

  constructor(url?: string) {
    this.url = url || (import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/gold-prices/');
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
          console.log('WebSocket connected');
          this.reconnectAttempts = 0;
          this.resubscribe();
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data);
            this.handleMessage(message);
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        this.ws.onclose = () => {
          console.log('WebSocket disconnected');
          this.handleReconnect();
        };

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          reject(error);
        };

      } catch (error) {
        reject(error);
      }
    });
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
      this.subscriptions.clear();
    }
  }

  private handleReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.connect().catch(console.error);
      }, this.reconnectDelay * this.reconnectAttempts);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  private handleMessage(message: WebSocketMessage): void {
    // Dispatch custom events for different message types
    const event = new CustomEvent(`ws_${message.type}`, {
      detail: message.data
    });
    window.dispatchEvent(event);
  }

  subscribe(channel: string): void {
    this.subscriptions.add(channel);
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.send({
        type: 'subscribe',
        channel: channel
      });
    }
  }

  unsubscribe(channel: string): void {
    this.subscriptions.delete(channel);
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.send({
        type: 'unsubscribe',
        channel: channel
      });
    }
  }

  private resubscribe(): void {
    this.subscriptions.forEach(channel => {
      this.send({
        type: 'subscribe',
        channel: channel
      });
    });
  }

  send(data: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.error('WebSocket not connected');
    }
  }

  placeOrder(orderData: {
    transaction_type: 'BUY' | 'SELL';
    gold_weight: number;
    gold_price_per_gram?: number;
  }): void {
    this.send({
      type: 'place_order',
      data: orderData
    });
  }

  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

// Create singleton instance
export const wsService = new WebSocketService();

// Custom React hook for WebSocket
export const useWebSocket = () => {
  const subscribe = (eventType: string, callback: (data: any) => void) => {
    const handler = (event: CustomEvent) => {
      callback(event.detail);
    };
    
    window.addEventListener(`ws_${eventType}`, handler as EventListener);
    
    return () => {
      window.removeEventListener(`ws_${eventType}`, handler as EventListener);
    };
  };

  return {
    subscribe,
    connect: () => wsService.connect(),
    disconnect: () => wsService.disconnect(),
    subscribe: (channel: string) => wsService.subscribe(channel),
    unsubscribe: (channel: string) => wsService.unsubscribe(channel),
    placeOrder: (orderData: any) => wsService.placeOrder(orderData),
    isConnected: () => wsService.isConnected(),
  };
};

export default wsService;