class CreateLogs < ActiveRecord::Migration
  def change
    create_table :logs do |t|
      t.string :name

      t.timestamps
    end
  end
end
