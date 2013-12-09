class CreateEntries < ActiveRecord::Migration
  def change
    create_table :entries do |t|
      t.datetime :date
      t.datetime :time
      t.string :protocol
      t.string :conn_type
      t.integer :src_port, null: true
      t.integer :dest_port, null: true
      t.string :src_ip
      t.string :dest_ip
      t.string :info
      t.string :environment

      t.timestamps
    end
  end
end
