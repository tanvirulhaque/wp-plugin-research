<?php
/* Plugin Name: Demo */
class Demo {
  function __construct() {
    add_action( 'wp_loaded', array( $this, 'reprice_cart' ) );
    add_action( 'init', [ $this, 'light' ] );
  }
  function reprice_cart() {
    foreach ( WC()->cart->get_cart( ) as $item ) { }
    WC()->cart->calculate_totals();
  }
  function light() { return 1; }
}
$x = wp_remote_post('https://stats.example.com', []);
